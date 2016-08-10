from django.conf.urls import url
from .views import StoreDashboard

urlpatterns = [
	url(r'^almacen/$', StoreDashboard.as_view(), name='store'),
]
