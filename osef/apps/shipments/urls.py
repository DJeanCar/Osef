from django.conf.urls import url
from .views import GetCargesAjax

urlpatterns = [
	url(r'^traer-cargos-ajax/$', GetCargesAjax.as_view(), name='get_charges'),
]
