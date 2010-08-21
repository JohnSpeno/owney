import datetime
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
    tracking = models.CharField(
        "tracking number", max_length=32, primary_key=True)
    cs_id = models.CharField("Request ID", max_length=32)
    status = models.CharField(
        max_length=64, default="new", choices=STATUS_CHOICES)
    description = models.TextField()
    created = models.DateTimeField();
    updated = models.DateTimeField();
    event_time = models.DateTimeField(null=True);

    objects = ShipmentManager()

    class Meta:
        ordering = ('created', 'cs_id')

    def save(self):
        now = datetime.datetime.now()
        if not self.tracking:
            self.created = now 
        self.updated = now
        super(Shipment, self).save()

    def __unicode__(self):
        url = self.tracking
        s = "%s (%s) created on %s" % (self.cs_id, url, self.created)
        if self.status == 'delivered':
            s += ", delivered on %s" % self.updated
        return s

    @property
    def ship_date(self):
        return self.created.date()

    @property
    def age(self):
        if self.status == 'delivered':
            delta = self.event_time - self.created
        else:
            delta = datetime.datetime.now() - self.created
        return delta.days

