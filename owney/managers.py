from django.db.models import Manager
       
class ShipmentManager(Manager):
"""Returns Shipments that are not delivered""" 
       
    def undelivered(self):
        return self.get_query_set().exclude(status__exact='delivered')
