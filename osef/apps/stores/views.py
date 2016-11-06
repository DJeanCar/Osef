import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from apps.shipments.models import Shipment
from apps.users.models import User, Notification, Comment
from .models import Movement, SocioMovement
from .forms import CreateMovForm
from .admin import MovementResource

class StoreDashboard(LoginRequiredMixin, TemplateView):

	template_name = 'stores/dashboard.html'
	login_url = '/'
	saldo_deudor = 0
	gastos = 0
	has_shipments = False

	def _get_movements_by_shipment(self, shipments):
		movements_by_shipment = []
		for shipment in shipments:
			abono = 0
			charge = 0
			movements = Movement.objects.filter(shipment = shipment)
			movements_by_shipment.append(movements)
			for movement in movements:
				if movement.kind_mov.name.lower() == 'cargo':
					charge += movement.amount
				if movement.kind_mov.name.lower() == 'abono':
					abono += movement.amount
			setattr(shipment, 'total_abono', abono)
			setattr(shipment, 'total_charge', charge)
			self.saldo_deudor += shipment.saldo # suma montos embarques
			self.gastos = self.gastos + charge
		return zip(shipments, movements_by_shipment)

	def get_context_data(self, **kwargs):
		context = super(StoreDashboard, self).get_context_data(**kwargs)
		if self.request.GET.get('search'):
			shipments = Shipment.objects.filter(store=self.request.user, amount__gt = 0, name__icontains = self.request.GET.get('search'), approved=True)
		else:
			shipments = Shipment.objects.filter(store=self.request.user, amount__gt = 0, approved=True)
		shipments_with_movements = self._get_movements_by_shipment(shipments)
		if shipments.count() == 0:
			context['no_shipments'] = True
		context['sorted_movements'] = list(shipments_with_movements)
		context['saldo_deudor'] = self.saldo_deudor
		context['gastos'] = self.gastos
		context['has_shipments'] = True if shipments.count() > 0 else False
		context['last_movement'] = Movement.objects.filter(store=self.request.user, approved=True).last()
		context['last_charge'] = Movement.objects.filter(store=self.request.user, kind_mov__name__iexact='cargo', approved=True).last()
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
		if self.request.session.get('is_saved'):
			context['is_saved'] = True
			self.request.session['is_saved'] = False
		return context

	def form_valid(self, form):
		movement = Movement.objects.create(
			store = self.request.user,
			kind_mov = form.cleaned_data.get('kind_mov'),
			kind_charge = form.cleaned_data.get('kind_charge'),
			charge = form.cleaned_data['charge'],
			shipment = form.cleaned_data.get('shipment'),
			description = form.cleaned_data.get('description'),
			amount = form.cleaned_data.get('amount'),
			image = form.cleaned_data.get('image')
		)
		self.request.session['is_saved'] = True
		socios = User.objects.filter(kind = "socio")
		for socio in socios:
			Notification.objects.create(
				user = self.request.user,
				sender = socio,
				store_movement = movement,
				description = "Nuevo movimiento del almacen"
			)
		return super(CreateStore, self).form_valid(form)

	def get_form(self, form_class=None):
		"""
		Returns an instance of the form to be used in this view.
		"""
		if form_class is None:
			form_class = self.get_form_class()
		return form_class(self.request.user, **self.get_form_kwargs())

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated():
			if request.user.kind == "almacen":
				shipments = Shipment.objects.filter(store=self.request.user, amount__gt = 0)
				if shipments.count() > 0:
					return super(CreateStore, self).dispatch(request, *args, **kwargs)
				else:
					return redirect(reverse('stores:dashboard'))
			else:
				return redirect(reverse('main:home'))
		else:
			return redirect(reverse('main:home'))


class AddImageMovement(View):

	def post(self, request, *args, **kwargs):
		movement = get_object_or_404(SocioMovement, id=kwargs['id'])
		movement.image = request.FILES['image']
		movement.save()
		return JsonResponse({'success' : True, 'image_url': movement.image.url})


class NotificationView(TemplateView):

	template_name = 'stores/notifications.html'

	def get_context_data(self, **kwargs):
		context = super(NotificationView, self).get_context_data(**kwargs)
		context['notification'] = get_object_or_404(Notification, id = kwargs['id'])
		context['comments'] = Comment.objects.filter(notification = context['notification'])
		return context

	def post(self, request, *args, **kwargs):
		approved = False
		no_approved = False
		notification = get_object_or_404(Notification, id = kwargs['id'])
		ctx = {'notification': notification}
		if 'approved' in request.POST:
			notification.socio_movement.approved = True
			notification.socio_movement.waiting = False
			notification.socio_movement.shipment.approved = True
			approved = True
			notification.socio_movement.save()
			notification.socio_movement.shipment.save()
		elif 'no_approved' in request.POST:
			notification.socio_movement.waiting = False
			no_approved = True
			notification.socio_movement.save()
		else:
			Comment.objects.create(
				user = request.user,
				notification = notification,
				content = request.POST['content']
			)
			comments = Comment.objects.filter(notification = notification)
			ctx['comments'] = comments
		ctx['approved'] = approved
		ctx['no_approved'] = no_approved
		return render(request, 'stores/notifications.html', ctx)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if request.user.kind == "almacen":
				return super(NotificationView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect(reverse('users:dashboard'))
		else:
			return redirect(reverse('main:home'))
