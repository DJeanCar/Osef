from django.contrib import admin

from import_export import resources, fields

from .models import KindMovement, Movement

class MovementResource(resources.ModelResource):

	amount = fields.Field(column_name='Monto')
	description = fields.Field(column_name='Descripción')
	charge = fields.Field(column_name='Tipo de cargo')
	shipment = fields.Field(column_name='Embarque')
	movement = fields.Field(column_name='Tipo de Movimiento')

	class Meta:
		model = Movement
		fields = ('created_at',)

	def dehydrate_movement(self, obj):
		return obj.kind_mov.name

	def dehydrate_charge(self, obj):
		if obj.kind_charge:
			return obj.kind_charge.name
		else:
			return '-'

	def dehydrate_shipment(self, obj):
		return obj.shipment.name

	def dehydrate_description(self, obj):
		return obj.description

	def dehydrate_amount(self, obj):
		return obj.amount


@admin.register(KindMovement)
class KindMovementAdmin(admin.ModelAdmin):
	pass

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
	
	list_display = ('kind_mov', 'charge', 'kind_charge', 
		'shipment', 'description', 'amount', 'created_at', 
		'updated_at', 'approved')
	list_editable = ('approved',)
