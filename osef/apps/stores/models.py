from django.db import models
from apps.shipments.models import Shipment, Charge, KindCharge
from apps.main.models import TimeStamp
from apps.users.models import User
from apps.shipments.models import Shipment

class KindMovement(models.Model):

	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Movement(TimeStamp):

	store = models.ForeignKey(User)
	kind_mov = models.ForeignKey(KindMovement)
	kind_charge = models.ForeignKey(KindCharge, null=True, blank=True)
	charge = models.ForeignKey(Charge, null=True, blank=True)
	shipment = models.ForeignKey(Shipment, null=True, blank=True)
	description = models.TextField()
	amount = models.IntegerField()
	approved = models.BooleanField(default=False)
	image = models.ImageField(upload_to='movements')

	def __str__(self):
		return '%s - %s' % (self.kind_mov, self.shipment)

	def save(self, *args, **kw):
		if self.pk is not None:
			orig = Movement.objects.get(pk=self.pk)
			if orig.approved != self.approved and not orig.approved:
				shipment = Shipment.objects.get(id=orig.shipment.id)
				shipment.saldo -= orig.amount
				shipment.save()
		super(Movement, self).save(*args, **kw)
