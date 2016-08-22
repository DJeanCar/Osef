from django.conf.urls import url
from .views import DashboardView, NoPermissionView, GetEmailView, UserProfileView
from . import views

urlpatterns = [
	url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
	url(r'^no-actvo/$', NoPermissionView.as_view(), name='no_permission'),
	url(r'^obtener-email/$', GetEmailView.as_view(), name='get_email'),
	url(r'^perfil/$', UserProfileView.as_view(), name='profile'),
	url(r'^salir/$', views.LogOut, name='logout'),
]
