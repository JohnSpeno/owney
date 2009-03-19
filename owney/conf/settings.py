from django.conf import settings

_TRACKING_USPS_URL = 'http://trkcnfrm1.smi.usps.com/PTSInternetWeb/InterLabelInquiry.do?origTrackNum='
TRACKING_USPS_URL = getattr(settings, 'TRACKING_USPS_URL', _TRACKING_USPS_URL)

_USPS_API_URL = 'http://production.shippingapis.com/ShippingAPI.dll'
USPS_API_URL = getattr(settings, 'USPS_API_URL', _USPS_API_URL 

_USPS_API_USERID = 'Set your USPS API userid here'
USPS_API_USERID = getattr(settings, 'USPS_API_USERID', _USPS_API_USERID) 

_CS_URL = 'Set the URL for your Customer Service application here'
TRACKING_CS_URL = getattr(settings, 'TRACKING_CS_URL', _CS_URL)



