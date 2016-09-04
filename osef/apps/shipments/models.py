from django.db import models
from apps.users.models import User

class Shipment(models.Model):

	store = models.ForeignKey(User, verbose_name='Almancén')
	name = models.CharField(max_length=50)
	amount = models.BigIntegerField()

	def __str__(self):
		return "%s - %s USD" % (self.name, self.amount)

class KindCharge(models.Model):

	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Charge(models.Model):

	CHARGES = (
			('directo', 'Directo'),
			('indirecto', 'Indirecto')
		)

	name = models.CharField(max_length=50)
	kind = models.ForeignKey(KindCharge)

	def __str__(self):
		return self.name