import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from apps.shipments.models import Shipment
from .models import Movement
from .forms import CreateMovForm
from .admin import MovementResource

class StoreDashboard(LoginRequiredMixin, TemplateView):

	template_name = 'stores/dashboard.html'
	login_url = '/'

	def _get_sorted_shipments(self, movements):
		shipments = set([movement.shipment for movement in movements])
		sort_movements = []
		for shipment in shipments:
			abono = 0
			charge = 0
			movements_by_shipment = []
			for movement in movements:
				if movement.shipment == shipment:
					movements_by_shipment.append(movement)
					if movement.kind_mov.name.lower() == 'cargo':
						charge += movement.amount
					if movement.kind_mov.name.lower() == 'abono':
						abono += movement.amount
			# print(abono)
			sort_movements.append(movements_by_shipment)
			setattr(shipment, 'total_abono', abono)
			setattr(shipment, 'total_charge', charge)
			setattr(shipment, 'total', charge + abono)
		return zip(shipments, sort_movements)

	def get_context_data(self, **kwargs):
		context = super(StoreDashboard, self).get_context_data(**kwargs)
		movements = Movement.objects.filter(store = self.request.user)
		if self.request.GET.get('search'):
			# Search movements
			movements = movements.filter(shipment__name__icontains = self.request.GET.get('search'))
			sorted_movements = self._get_sorted_shipments(movements)
		else:
			# All movements
			sorted_movements = self._get_sorted_shipments(movements)
		context['sorted_movements'] = sorted_movements
		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.has_permission:
			if request.user.kind == "almacen":
				return super(StoreDashboard, self).dispatch(request, *args, **kwargs)
			else:
				return redirect(reverse('users:dashboard'))
		else:
			return redirect(reverse('users:no_permission'))
	

class StoreExportDashboard(View):

	def get(self, request, *args, **kwargs):
		queryset = Movement.objects.all().order_by('shipment')
		dataset = MovementResource().export(queryset)
		response = HttpResponse(dataset.csv, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="movimientos.csv"'
		return response


class CreateStore(FormView):

	template_name = 'stores/create_store.html'
	form_class = CreateMovForm
	success_url = reverse_lazy('stores:create_store')

	def get_context_data(self, **kwargs):
		context = super(CreateStore, self).get_context_data(**kwargs)
		context['shipments'] = Shipment.objects.filter(amount__gt = 0)
		if self.request.session.get('is_saved'):
			context['is_saved'] = True
			self.request.session['is_saved'] = False
		return context

	def form_valid(self, form):
		Movement.objects.create(
			store = self.request.user,
			kind_mov = form.cleaned_data.get('kind_mov'),
			kind_charge = form.cleaned_data.get('kind_charge'),
			charge = form.cleaned_data['charge'],
			shipment = form.cleaned_data.get('shipment'),
			description = form.cleaned_data.get('description'),
			amount = form.cleaned_data.get('amount')
		)
		self.request.session['is_saved'] = True
		return super(CreateStore, self).form_valid(form)