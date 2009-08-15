"""
get tracking for each undelivered shipment that has no exception
if tracksummary's event is delivered, mark shipment as delivered.
else check through each event looking for exception type events (notice left, no such number, etc)
if any exception events are found, make this shipment as having an exception

(if the package had exception, the summary may not show it as packages are returned to us. the summary should show the last
thing the package did, like get 'processed')

"""

import urllib
import urllib2
import sys
import datetime
from django.conf import settings
from xml.etree import ElementTree as et

from owney.conf.settings import USPS_API_USERID, USPS_API_URL

# Number of tracking numbers to lookup at once
MAX_TRACK = 10

DB_NAME = "shipments.db"
DB_ENGINE='sqlite3'

EV_NSN = "No Such Number"
EV_NOTICE = "Notice Left"
EV_UNDELIVERABLE = "Undeliverable as Addressed"
EV_EXCEPTIONS = (EV_NSN, EV_NOTICE, EV_UNDELIVERABLE)

event_types = { 
    'Electronic Shipping Info Received' : 'acknowledged',
    'Shipment Accepted' : 'accepted',
    'Acceptance' : 'accepted',
    'Processed' : 'processed',
    'Processed through Sort Facility' : 'processed',
    'Arrival at Unit' : 'arrival',
    'Arrival at Pick-Up-Point' : 'arrival',
    'Notice Left' : 'exception',
    'No Such Number' : 'exception',
    'Undeliverable as Addressed' : 'exception',
    'Missent' : 'exception',
    'Return to Sender' : 'exception',
    'Forwarded' : 'forwarded',
    'Delivered' : 'delivered',
}

XML="""
<TrackFieldRequest USERID="%s">%%s</TrackFieldRequest>
""" % USPS_API_USERID

def _textlist(self, _addtail=False):
    """
    Returns a list of text strings contained within an element and its
    sub-elements.

    Source: http://code.activestate.com/recipes/498286/
    """
    result = []
    if self.text is not None:
        result.append(self.text)
    for elem in self:
        result.extend(elem.textlist(True))
    if _addtail and self.tail is not None:
        result.append(self.tail)
    return result

# inject the new method into the ElementTree framework
from xml.etree.ElementTree import _Element
_Element.textlist = _textlist


def split_seq(seq, size):
    """Split up seq in pieces of size.
    Source:  http://code.activestate.com/recipes/425044"""
    return [seq[i:i+size] for i in range(0, len(seq), size)]

_months = [None,
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]
            
def get_event_date(summary):
    """
    Given elementree object from delivery summary, construct a datetime
    object from its EventTime and EventDate fields.
    """
    etime = summary.find('EventTime').text
    hour, rest = etime.split(':')
    hour = int(hour)
    minute, am_or_pm = rest.split(' ')
    minute = int(minute)
    if am_or_pm == 'pm' and hour != 12:
        hour += 12
    elif am_or_pm == 'am' and hour == 12:
        hour = 0 
    edate = summary.find('EventDate').text
    first, year = edate.split(',')
    year = int(year)
    month, day = first.split(' ')
    day = int(day)
    month = _months.index(month)
    return datetime.datetime(year, month, day, hour, minute)

def get_tracking(batch):
    s = []
    for tracking_num in batch:
       s.append('<TrackID ID="%s"></TrackID>' % tracking_num)
    args = {
        'API' : 'TrackV2',
        'XML' : XML % (''.join(s))
    }
    params = urllib.urlencode(args)
    req = urllib2.Request(USPS_API_URL, params)
    try:
        return urllib2.urlopen(req)
    except urllib2.URLError, e:
        print >>sys.stderr, "urlopen error: %s" % e
        return None

def get_usps_status(tracking_nums):
    """given sequence of tracking numbers return mapping of tracking numbers
    to last status.
    """
    errs = {} 
    res = {}
    for batch in split_seq(tracking_nums, MAX_TRACK): 
        data = get_tracking(batch)
        if data is None:
            continue
        tree = et.parse(data)
        top = tree.getroot()
        if top.tag == 'Error': 
            enumber = top.find('Number').text
            edesc = top.find('Description').text
            print >>sys.stderr, "API ERROR: %s (%s)" % (edesc, enumber)
            continue 
        for tracking in tree.getiterator('TrackInfo'):
            track_id = tracking.get('ID')
            # also need to check for an Error tag here
            err = tracking.find('Error')
            if err is not None:
                enumber = err.find('Number').text
                edesc = err.find('Description').text
                errs[track_id] = (enumber, edesc) 
                continue
            summary = tracking.find('TrackSummary')
            if summary is None:
                errs[track_id] = (1, 'No TrackSummary found')
                continue
            event = summary.find('Event').text
            if event is None:
                errs[track_id] = (2, 'No Event found')
                continue
            description = ' '.join(summary.textlist())
            event_date = get_event_date(summary)
            if event not in event_types:
                # unknown event type. make note of it
                s = "UNKNONWN event '%s'" % event
                errs[track_id] = (2, s)

            else:
                status = event_types[event]
                res[track_id] = (status, event_date, description)
    return res, errs

if __name__ == '__main__':
    settings.configure(DATABASE_ENGINE=DB_ENGINE, DATABASE_NAME=DB_NAME)
    from owney.models import Shipment
    shipments = Shipment.objects.exclude(status='delivered').order_by(
        'created', 'cs_id')
    trackings = [x.tracking for x in shipments]
    results, errors = get_usps_status(trackings)
    for track_id, result in results.iteritems():
        try:
            shipment = Shipment.objects.get(pk=track_id)
        except Shipment.DoesNotExist:
            print >>sys.stderr, "Unknown shipment '%s'" % track_id
            continue
        old_status = shipment.status
        old_time = shipment.event_time
        status, event_time, description = result
        shipment.status = status
        shipment.event_time = event_time
        shipment.description = description
        if (old_status != status) or (old_time != event_time):
            if status == 'exception':
                print "**** ",
            print '%s: {%s} %s %s -> %s %s' % (shipment.ship_date,
                shipment.cs_id, track_id, old_status, status, event_time)
            shipment.save()

    missing = 0
    for track_id, error in errors.iteritems():
        enumber, etext = error
        # 2147219302 is "No record of that item"
        # It's what you get after label is printed but before it is in the
        # "system" at USPS
        # and we don't need to see it
        if enumber != '-2147219302':
            print "%s ERROR: %s (%s)" % (track_id, etext, enumber)
        else:
            missing = missing + 1
    if missing:
        print "FYI: %d packages have no records yet" % missing
