from django.contrib import admin
from .models import Shipment, Charge, KindCharge, Abono

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
	list_display = ('store', 'name', 'amount')

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
	pass
	
@admin.register(KindCharge)
class KindChargeAdmin(admin.ModelAdmin):
	pass

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
  pass