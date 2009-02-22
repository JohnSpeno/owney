from django.contrib import admin
from models import Shipment

admin.site.register(Shipment)

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('event_time')
