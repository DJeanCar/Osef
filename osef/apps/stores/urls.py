from django.conf.urls import url
from .views import StoreDashboard, CreateStore

urlpatterns = [
	url(r'^almacen/$', StoreDashboard.as_view(), name='dashboard'),
	url(r'^almacen/agregar-movimiento/$', CreateStore.as_view(), name='create_store'),
]
