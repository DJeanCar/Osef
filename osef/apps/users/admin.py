from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Notification, Comment

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
	list_display = ('user', 'description', 'sender')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass
