from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from apps.shipments.models import Shipment
from .models import Movement
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

	def form_valid(self, form):
		Movement.objects.create(
			kind_mov = form.cleaned_data.get('kind_mov'),
			kind_charge = form.cleaned_data.get('kind_charge'),
			charge = form.cleaned_data['charge'],
			shipment = form.cleaned_data.get('shipment'),
			description = form.cleaned_data.get('description'),
			amount = form.cleaned_data.get('amount')
		)
		return super(CreateStore, self).form_valid(form)