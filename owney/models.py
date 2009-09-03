from django.db import models
from managers import ShipmentManager

STATUS_CHOICES = (
    # new = a label has been printed
    ("new", "new"),
    # acknowledged = electronic shipping info received
    ("acknowledged", "acknowledged"),
    # accepted = scan form acceptance
    ("accepted", "accepted"),
    # processed = package got handled someplace
    ("processed", "processed"),
    ("arrival", "arrival"),
    # package was forwarded
    ("forwarded", "forwarded"),
    # delivered = delivered
    ("delivered", "delivered"),
    # exception = Missent | notice left | no such number | undeliverable
    ("exception", "exception"),
)

class Shipment(models.Model):
    """
    A USPS Shipment
    """
    tracking = models.CharField("tracking number", max_length=32,
                                primary_key=True)
    cs_id = models.CharField("Request ID", max_length=32)
    status = models.CharField(max_length=64, default="new",
                                choices=STATUS_CHOICES)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True);
    updated = models.DateTimeField(auto_now=True);
    event_time = models.DateTimeField(null=True);

    objects = ShipmentManager()

    def __unicode__(self):
        url = self.tracking
        s = "%s (%s) created on %s" % (self.cs_id, url, self.created)
        if self.status == 'delivered':
            s += ", delivered on %s" % self.updated
        return s 

    @property
    def ship_date(self):
        return self.created.date()

    class Admin:
        pass

