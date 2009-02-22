from django.conf.urls.defaults import *
from models import Shipment
from admin import *

from django.contrib import admin
admin.autodiscover()

import tracking.track.views 

urlpatterns = patterns('owney.views',
    url(r'^admin/(.*)', admin.site.root), 
    url(r'^$', 'index', name="shipment_index"),
)
