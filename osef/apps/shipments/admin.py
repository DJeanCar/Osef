from django.contrib import admin
from .models import Shipment, Charge

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
	pass

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
	pass
	