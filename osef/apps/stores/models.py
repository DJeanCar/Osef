from django.db import models
from apps.shipments.models import Shipment, Charge, KindCharge
from apps.main.models import TimeStamp

class KindMovement(models.Model):

	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Movement(TimeStamp):

	kind_mov = models.ForeignKey(KindMovement)
	kind_charge = models.ForeignKey(KindCharge, null=True, blank=True)
	charge = models.ForeignKey(Charge, null=True, blank=True)
	shipment = models.ForeignKey(Shipment, null=True, blank=True)
	description = models.TextField()
	amount = models.IntegerField()
	approved = models.BooleanField(default=False)

	def __str__(self):
		return '%s - %s' % (self.kind_mov, self.shipment)
