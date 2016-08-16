from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from apps.shipments.models import Shipment
from .forms import CreateMovForm

class StoreDashboard(TemplateView):

	template_name = 'stores/dashboard.html'
	
class CreateStore(FormView):

	template_name = 'stores/create_store.html'
	form_class = CreateMovForm

	def get_context_data(self, **kwargs):
		context = super(CreateStore, self).get_context_data(**kwargs)
		context['shipments'] = Shipment.objects.filter(amount__gt = 0)
		return context