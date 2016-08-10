from django.conf.urls import url
from .views import DashboardView, NoPermissionView
from . import views

urlpatterns = [
	url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
	url(r'^no-actvo/$', NoPermissionView.as_view(), name='no_permission'),
	url(r'^salir/$', views.LogOut, name='logout'),
]
