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
    A USPS Shipment.
    """
    tracking = models.CharField(
        "tracking number", max_length=32, primary_key=True
    )
    cs_id = models.CharField("Request ID", max_length=32)
    status = models.CharField(
        max_length=64, default="new", choices=STATUS_CHOICES
    )
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
        s = u"%s {%s} created on %s" % (
            self.tracking, self.cs_id, self.ship_date
        )
        if self.status == 'delivered':
            s += ", delivered on %s" % self.event_time.date()
        return s

    @property
    def ship_date(self):
        """Return date of shipment."""
        return self.created.date()

    @property
    def age(self):
        """Return age of shipment in days."""
        then = self.ship_date
        if self.status == 'delivered':
            now = self.event_time.date()
        else:
            now = datetime.datetime.now().date()
        delta = now - then
        return delta.days
