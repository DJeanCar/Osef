from django.contrib import admin
from .models import KindMovement, Movement

@admin.register(KindMovement)
class KindMovementAdmin(admin.ModelAdmin):
	pass

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
	pass
