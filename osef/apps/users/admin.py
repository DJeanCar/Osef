from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Notification, Comment
from import_export import resources, fields
from apps.stores.models import SocioMovement

class MovementResource(resources.ModelResource):

	amount = fields.Field(column_name='Monto')
	currency = fields.Field(column_name='Moneda')
	description = fields.Field(column_name='Descripción')
	charge = fields.Field(column_name='Tipo de cargo')
	shipment = fields.Field(column_name='Embarque')
	movement = fields.Field(column_name='Tipo de Movimiento')

	class Meta:
		model = SocioMovement
		fields = ('created_at',)

	def dehydrate_currency(self, obj):
		if obj.account:
			return obj.account.name
		else:
			return 'Dólares'

	def dehydrate_movement(self, obj):
		return obj.kind_mov.name

	def dehydrate_charge(self, obj):
		if obj.kind_charge:
			return obj.kind_charge.name
		else:
			return '-'

	def dehydrate_shipment(self, obj):
		if obj.shipment:
			return obj.shipment.name
		else:
			return None

	def dehydrate_description(self, obj):
		return obj.description

	def dehydrate_amount(self, obj):
		return obj.amount

@admin.register(User)
class UserAdmin(UserAdmin):

	list_display = ('username', 'first_name', 'last_name', 'email', 'has_permission', 'kind')
	search_fields = ('username', 'email')
	list_editable = ('has_permission', 'kind')
	list_filter = ('is_superuser',)
	ordering = ('username',)
	filter_horizontal = ('groups', 'user_permissions')

	fieldsets = (
			('User', {'fields' : ('username', 'password')}),
			('Personal Info', {'fields' : (
							'first_name',
							'last_name',
							'email',
							'url_photo',
							'photo',
							'has_permission',
							'kind',
					)}),
			('Permissions', {'fields': (
							'is_active',
							'is_staff',
							'is_superuser',
							'has_permission',
							'groups',
							'user_permissions',
				)}),
		)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

	list_display = ('currency', 'amount', )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('user', 'description', 'sender', 'viewed')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass
