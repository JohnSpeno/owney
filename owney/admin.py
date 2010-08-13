from django.contrib import admin
from models import Shipment

class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'cs_id', 'tracking', 'created', 'status',
        'updated', 'age'
    )
    list_filter = ('status', 'created', 'event_time')
    list_per_page = 50
    list_display_links = ('cs_id', 'tracking')
    ordering = ('updated',)
    date_hierarchy = 'created'

admin.site.register(Shipment, ShipmentAdmin)
