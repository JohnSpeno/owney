from django.conf.urls.defaults import *
from models import Shipment

from django.contrib import admin
admin.autodiscover()

import owney.views 

urlpatterns = patterns('owney.views',
    url(r'^$', 'index', name="shipment_index"),
)
