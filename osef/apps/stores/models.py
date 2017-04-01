from django.db import models
from apps.shipments.models import Shipment, Charge, KindCharge
from apps.main.models import TimeStamp
from apps.users.models import User, Account
from apps.shipments.models import Shipment, Abono

class KindMovement(models.Model):

	name = models.CharField(max_length=50)
	store = models.BooleanField(default=False)

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
	waiting = models.BooleanField(default=True)
	image = models.ImageField(upload_to='movements')

	def __str__(self):
		return '%s - %s' % (self.kind_mov, self.shipment)

	def save(self, *args, **kw):
		if self.pk is not None:
			orig = Movement.objects.get(pk=self.pk)
			if orig.approved != self.approved and not orig.approved and orig.shipment:
				shipment = Shipment.objects.get(id=orig.shipment.id)
				shipment.saldo -= orig.amount
				shipment.save()
		super(Movement, self).save(*args, **kw)


class SocioMovement(TimeStamp):

	socio = models.ForeignKey(User)
	retiro = models.ForeignKey(User, null=True, blank=True, related_name='retiro_socio')
	account = models.ForeignKey(Account, null=True, blank=True)
	kind_abono = models.ForeignKey(Abono, null=True, blank=True)
	kind_mov = models.ForeignKey(KindMovement)
	kind_charge = models.ForeignKey(KindCharge, null=True, blank=True)
	charge = models.ForeignKey(Charge, null=True, blank=True)
	shipment = models.ForeignKey(Shipment, null=True, blank=True)
	description = models.TextField()
	amount = models.IntegerField()
	precio_costo = models.IntegerField(null=True, blank=True)
	type_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	approved = models.BooleanField(default=False)
	waiting = models.BooleanField(default=True)
	image = models.ImageField(upload_to='movements', null=True, blank=True)

	def __str__(self):
		return '%s - %s' % (self.kind_mov, self.socio)
