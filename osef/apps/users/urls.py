from django.conf.urls import url
from .views import DashboardView, NoPermissionView, GetEmailView, UserProfileView, CreateMovementView, DetailMovementView
from . import views

urlpatterns = [
  url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
  url(r'^dashboard/movimiento/(?P<id>[0-9]+)/$', DetailMovementView.as_view(), name='movement_detail'),
	url(r'^dashboard/crear-movimiento/$', CreateMovementView.as_view(), name='create_movement'),
	url(r'^no-actvo/$', NoPermissionView.as_view(), name='no_permission'),
	url(r'^obtener-email/$', GetEmailView.as_view(), name='get_email'),
	url(r'^perfil/$', UserProfileView.as_view(), name='profile'),
	url(r'^salir/$', views.LogOut, name='logout'),
]
