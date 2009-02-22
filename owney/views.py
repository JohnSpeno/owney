from tracking.track.models import Shipment
from django.shortcuts import render_to_response, get_object_or_404
from track.conf import settings

USPS_URL = getattr(settings, 'TRACKING_USPS_URL')
CS_URL = getattr(settings, 'TRACKING_CS_URL')

def index(request, template_name="shipment_list.html"):
    """
    Display index of undelivered shipments by day.
    """
    shipments = Shipment.objects.exclude(status='delivered').order_by(
                    'created', 'cs_id')
    num_undelivered = shipments.count() 
    return render_to_response(template_name,
                                {'num_undelivered' : num_undelivered,
                                 'ship_list' : shipments,
                                 'usps_url' : USPS_URL,
                                 'cs_url' : CS_URL})
