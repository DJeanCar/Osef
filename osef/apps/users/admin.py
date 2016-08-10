from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):

	list_display = ('username', 'first_name', 'last_name', 'email', 'has_permission')
	search_fields = ('username', 'email')
	list_editable = ('has_permission',)
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