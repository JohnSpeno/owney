from owney.models import Shipment
from owney.conf import settings

from django.shortcuts import render_to_response

USPS_URL = getattr(settings, 'TRACKING_USPS_URL')
CS_URL = getattr(settings, 'TRACKING_CS_URL')

def index(request, template_name="shipment_list.html"):
    """
    Display index of undelivered shipments by day.
    """
    shipments = Shipment.objects.undelivered()
    num_undelivered = shipments.count() 
    return render_to_response(template_name,
                                {'num_undelivered' : num_undelivered,
                                 'ship_list' : shipments,
                                 'usps_url' : USPS_URL,
                                 'cs_url' : CS_URL})
