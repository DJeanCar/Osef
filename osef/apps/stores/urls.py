from django.conf.urls import url
from .views import StoreDashboard, CreateStore, StoreExportDashboard, AddImageMovement, NotificationView

urlpatterns = [
	url(r'^almacen/dashboard/$', StoreDashboard.as_view(), name='dashboard'),
	url(r'^almacen/dashboard/notificaciones/(?P<id>[0-9]+)/$', NotificationView.as_view(), name='notifications'),
	url(r'^almacen/exportar/$', StoreExportDashboard.as_view(), name='dashboard_export'),
  	url(r'^almacen/agregar-movimiento/$', CreateStore.as_view(), name='create_store'),
	url(r'^movimiento/agregar-imagen/(?P<id>[0-9]+)/$', AddImageMovement.as_view(), name='movement_image'),
]
