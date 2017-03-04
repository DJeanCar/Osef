from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, FormView, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.shipments.models import Shipment
from apps.stores.models import SocioMovement
from .models import Account, Notification
from .forms import EmailForm, CreateMovForm, UpdateImage
from .admin import MovementResource
from itertools import chain
from datetime import datetime, timedelta
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q

class MeDashboardView(LoginRequiredMixin, TemplateView):

	template_name = 'users/me.html'
	login_url = '/'

	def get(self, request, *args, **kwargs):
		if request.user.kind == 'socio':
			return super(MeDashboardView, self).get(request, *args, **kwargs)
		else:
			return redirect(reverse('main:home'))

	def _get_sum_movements(self):
		retiro_dolar = 0
		retiro_pesos = 0
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'retiro'
		)
		for movement in movements:
			if movement.account.currency == 'usd':
				retiro_dolar += movement.amount
			if movement.account.currency == 'mxn':
				retiro_pesos += movement.amount
		return [retiro_dolar, retiro_pesos]

	def _get_sum_movements_abono(self):
		abono_dolar = 0
		abono_pesos = 0
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'abono'
		)
		for movement in movements:
			if movement.account.currency == 'usd':
				abono_dolar += movement.amount
			if movement.account.currency == 'mxn':
				abono_pesos += movement.amount
		return [abono_dolar, abono_pesos]

	def _get_total_abonos_dolar(self):
		total_abono_dolar = 0;
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'abono', 
			account__currency__iexact='usd'
		)
		for movement in movements:
			total_abono_dolar += movement.amount
		return total_abono_dolar

	def _get_total_abonos_pesos(self):
		total_abono_pesos = 0;
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'abono', 
			account__currency__iexact='mxn'
		)
		for movement in movements:
			total_abono_pesos += movement.amount
		return total_abono_pesos

	def _get_total_retiro_dolar(self):
		total_retiro_dolar = 0
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'retiro', 
			account__currency__iexact='usd'
		)
		for movement in movements:
			total_retiro_dolar += movement.amount
		return total_retiro_dolar

	def _get_total_retiro_pesos(self):
		total_retiro_pesos = 0
		movements = SocioMovement.objects.filter(
			socio = self.request.user,
			kind_mov__name__iexact = 'retiro', 
			account__currency__iexact = 'mxn'
		)
		for movement in movements:
			total_retiro_pesos += movement.amount
		return total_retiro_pesos

	def get_context_data(self, **kwargs):
		context = super(MeDashboardView, self).get_context_data(**kwargs)
		if self.request.GET.get('date'):
			# filter date
			if self.request.GET.get('date') == 'all':
				dolar_movements = SocioMovement.objects.filter(Q(account__currency__iexact='usd') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
			elif self.request.GET.get('date') == 'one_month':
				context['one_month'] = True
				last_month = datetime.today() - timedelta(days=30)
				dolar_movements = SocioMovement.objects.filter(Q(created_at__gte=last_month) & Q(account__currency__iexact='usd') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
			else:
				context['two_month'] = True
				last_month = datetime.today() - timedelta(days=60)
				dolar_movements = SocioMovement.objects.filter(Q(created_at__gte=last_month) & Q(account__currency__iexact='usd') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
		else:
			dolar_movements = SocioMovement.objects.filter(Q(account__currency__iexact='usd') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
		context['dolar_movements'] = dolar_movements
		
		if self.request.GET.get('date'):
			# filter date
			if self.request.GET.get('date') == 'all':
				pesos_movements = SocioMovement.objects.filter(Q(account__currency__iexact='mxn') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
			elif self.request.GET.get('date') == 'one_month':
				context['one_month'] = True
				last_month = datetime.today() - timedelta(days=30)
				pesos_movements = SocioMovement.objects.filter(Q(created_at__gte=last_month) & Q(account__currency__iexact='mxn') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
			else:
				context['two_month'] = True
				last_month = datetime.today() - timedelta(days=60)
				pesos_movements = SocioMovement.objects.filter(Q(created_at__gte=last_month) & Q(account__currency__iexact='mxn') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
		else:
			pesos_movements = SocioMovement.objects.filter(Q(account__currency__iexact='mxn') & (Q(kind_mov__name__iexact = 'retiro') | Q(kind_mov__name__iexact = 'abono'))).order_by('-created_at')
		context['pesos_movements'] = pesos_movements

		[retiro_dolar, retiro_pesos] = self._get_sum_movements();
		[abono_dolar, abono_pesos] = self._get_sum_movements_abono()
		context['abono_dolar'] = abono_dolar
		context['abono_pesos'] = abono_pesos
		context['retiro_dolar'] = retiro_dolar
		context['retiro_pesos'] = retiro_pesos
		context['total_abono_dolar'] = self._get_total_abonos_dolar()
		context['total_abono_pesos'] = self._get_total_abonos_pesos()
		context['total_retiro_dolar'] = self._get_total_retiro_dolar()
		context['total_retiro_pesos'] = self._get_total_retiro_pesos()
		context['last_retiro_dolar'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='usd').last()
		context['last_retiro_pesos'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='mxn').last()
		context['last_ingreso_dolar'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'abono', account__currency__iexact='usd').last()
		context['last_ingreso_pesos'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'abono', account__currency__iexact='mxn').last()
		return context

class DashboardView(LoginRequiredMixin, TemplateView):

	template_name = 'users/dashboard.html'
	login_url = '/'

	def _get_sum_movements(self):
		retiro_dolar = 0
		retiro_pesos = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro')
		for movement in movements:
			if movement.account.currency == 'usd':
				retiro_dolar += movement.amount
			if movement.account.currency == 'mxn':
				retiro_pesos += movement.amount
		return [retiro_dolar, retiro_pesos]

	def _get_sum_shipments(self):
		total_dolar = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'embarque')
		for movement in movements:
			total_dolar += movement.amount

		notifications_abono = Notification.objects.filter(store_movement__kind_mov__name__iexact = 'Abono', store_movement__approved=True)
		for notification in notifications_abono:
			total_dolar -= notification.store_movement.amount
		return total_dolar

	def _get_total_abonos_dolar(self):
		total_abono_dolar = 0;
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'abono', account__currency__iexact='usd')
		for movement in movements:
			total_abono_dolar += movement.amount
		return total_abono_dolar

	def _get_total_abonos_pesos(self):
		total_abono_pesos = 0;
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'abono', account__currency__iexact='mxn')
		for movement in movements:
			total_abono_pesos += movement.amount
		return total_abono_pesos

	def _get_total_cargos_dolar(self):
		total_cargos_dolar = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'cargo', account__currency__iexact='usd')
		for movement in movements:
			total_cargos_dolar += movement.amount
		return total_cargos_dolar

	def _get_total_cargos_pesos(self):
		total_cargos_pesos = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'cargo', account__currency__iexact='mxn')
		for movement in movements:
			total_cargos_pesos += movement.amount
		return total_cargos_pesos

	def _get_total_retiro_dolar(self):
		total_retiro_dolar = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='usd')
		for movement in movements:
			total_retiro_dolar += movement.amount
		return total_retiro_dolar

	def _get_total_retiro_pesos(self):
		total_retiro_pesos = 0
		movements = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='mxn')
		for movement in movements:
			total_retiro_pesos += movement.amount
		return total_retiro_pesos


	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		[pesos, dolar] = Account.objects.all()
		[retiro_dolar, retiro_pesos] = self._get_sum_movements();
		context['dolar'] = Account.objects.get(currency__iexact='usd')
		context['pesos'] = Account.objects.get(currency__iexact='mxn')
		context['retiro_dolar'] = retiro_dolar
		context['retiro_pesos'] = retiro_pesos
		context['embarque_total'] = self._get_sum_shipments()
		context['no_movements'] = True if SocioMovement.objects.count() == 0 else False
		
		if self.request.GET.get('date'):
			# filter date
			if self.request.GET.get('date') == 'all':
				dolar_movements = SocioMovement.objects.filter(account__currency__iexact='usd').order_by('-created_at')
			elif self.request.GET.get('date') == 'one_month':
				context['one_month'] = True
				last_month = datetime.today() - timedelta(days=30)
				dolar_movements = SocioMovement.objects.filter(created_at__gte=last_month, account__currency__iexact='usd').order_by('-created_at')
			else:
				context['two_month'] = True
				last_month = datetime.today() - timedelta(days=60)
				dolar_movements = SocioMovement.objects.filter(created_at__gte=last_month, account__currency__iexact='usd').order_by('-created_at')
		else:
			dolar_movements = SocioMovement.objects.filter(account__currency__iexact='usd').order_by('-created_at')
		context['dolar_movements'] = dolar_movements
		
		if self.request.GET.get('date'):
			# filter date
			if self.request.GET.get('date') == 'all':
				pesos_movements = SocioMovement.objects.filter(account__currency__iexact='mxn').order_by('-created_at')
			elif self.request.GET.get('date') == 'one_month':
				context['one_month'] = True
				last_month = datetime.today() - timedelta(days=30)
				pesos_movements = SocioMovement.objects.filter(created_at__gte=last_month, account__currency__iexact='mxn').order_by('-created_at')
			else:
				context['two_month'] = True
				last_month = datetime.today() - timedelta(days=60)
				pesos_movements = SocioMovement.objects.filter(created_at__gte=last_month, account__currency__iexact='mxn').order_by('-created_at')
		else:
			pesos_movements = SocioMovement.objects.filter(account__currency__iexact='mxn').order_by('-created_at')
		context['pesos_movements'] = pesos_movements
		
		if context['dolar_movements'].count() + context['pesos_movements'].count() == 0:
			context['exportToCSV'] = False
		else:
			context['exportToCSV'] = True
		context['last_movement_dolar'] = SocioMovement.objects.filter(account__currency__iexact='usd').last()
		context['last_movement_pesos'] = SocioMovement.objects.filter(account__currency__iexact='mxn').last()
		context['last_retiro_dolar'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='usd').last()
		context['last_retiro_pesos'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'retiro', account__currency__iexact='mxn').last()
		context['last_embarque'] = SocioMovement.objects.filter(kind_mov__name__iexact = 'embarque').last()
		context['total_abono_dolar'] = self._get_total_abonos_dolar()
		context['total_abono_pesos'] = self._get_total_abonos_pesos()
		context['total_cargos_dolar'] = self._get_total_cargos_dolar()
		context['total_cargos_pesos'] = self._get_total_cargos_pesos()
		context['total_retiro_dolar'] = self._get_total_retiro_dolar()
		context['total_retiro_pesos'] = self._get_total_retiro_pesos()
		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.has_permission:
			if request.user.kind == "socio":
				return super(DashboardView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect(reverse('stores:dashboard'))
		else:
			return redirect(reverse('users:no_permission'))

class UserProfileView(LoginRequiredMixin, TemplateView):

    template_name = "users/profile.html"
    login_url = '/'

    def post(self, request, *args, **kwargs):
    	request.user.first_name = request.POST['first_name']
    	request.user.last_name = request.POST['last_name']
    	if request.FILES.get('photo'):
    		request.user.photo = request.FILES['photo']
    	request.user.save()
    	return render(request, 'users/profile.html', { 'success' : True })

class NoPermissionView(LoginRequiredMixin, TemplateView):

	template_name = 'users/no_permission.html'
	login_url = '/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.has_permission:
			return redirect(reverse('users:dashboard'))
		else:
			return super(NoPermissionView, self).dispatch(request, *args, **kwargs)


class GetEmailView(FormView):

	template_name = 'users/get_email.html'
	form_class = EmailForm

	def form_valid(self, form):
		self.request.session['saved_email'] = form.cleaned_data['email']
		backend = self.request.session['partial_pipeline']['backend']
		url = '/complete/%s/' % backend
		self.request.session['has_access'] = False
		return redirect(url)

	def get_context_data(self, **kwargs):
		context = super(GetEmailView, self).get_context_data(**kwargs)
		context['fullname'] = self.request.session.get('fullname')
		context['url_photo'] = self.request.session.get('url_photo')
		return context

	def dispatch(self, request, *args, **kwargs):
		if request.session.get('has_access'):
			return super(GetEmailView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect(reverse('main:home'))

def LogOut(request):
	logout(request)
	return redirect(reverse('main:home'))

class CreateMovementView(FormView):

	template_name = 'users/create_movements.html'
	form_class = CreateMovForm
	success_url = reverse_lazy('users:create_movement')

	def get_context_data(self, **kwargs):
		context = super(CreateMovementView, self).get_context_data(**kwargs)
		if self.request.session.get('is_saved_shipment'):
			context['is_saved_shipment'] = True
			self.request.session['is_saved_shipment'] = False
		if self.request.session.get('is_saved'):
			context['is_saved'] = True
			self.request.session['is_saved'] = False
		return context

	def form_valid(self, form):
		if form.cleaned_data['kind_mov'].name.lower() == 'embarque':
			account = Account.objects.get(currency__iexact='usd')
			shipment = Shipment.objects.create(
					store = form.cleaned_data['store'],
					name = form.cleaned_data['name'],
					amount = form.cleaned_data['amount_shipment'],
					approved = False
				)
			movement = SocioMovement.objects.create(
				socio = self.request.user,
				shipment = shipment,
				account = account,
				description = form.cleaned_data.get('description'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				amount = form.cleaned_data.get('amount_shipment'),
			)
			account.amount -= int(form.cleaned_data.get('amount_shipment'))
			account.save()
			Notification.objects.create(
				user = self.request.user,
				sender = form.cleaned_data['store'],
				socio_movement = movement,
				description = 'Se le envio un embarque de ...',
			)
			self.request.session['is_saved_shipment'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'retiro':
			account = form.cleaned_data.get('account')
			SocioMovement.objects.create(
				socio = self.request.user,
			  account = form.cleaned_data.get('account'),
				retiro = form.cleaned_data.get('socio'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				kind_charge = form.cleaned_data.get('kind_charge'),
				charge = form.cleaned_data['charge'],
				description = form.cleaned_data.get('description'),
				amount = form.cleaned_data.get('amount'),
				image = form.cleaned_data.get('image'),
			)
			account.amount -= int(form.cleaned_data.get('amount'))
			account.save()
			self.request.session['is_saved'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'abono':
			account = form.cleaned_data.get('account')
			SocioMovement.objects.create(
				socio = self.request.user,
			  account = form.cleaned_data.get('account'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				kind_abono = form.cleaned_data.get('kind_abono'),
				description = form.cleaned_data.get('description'),
				amount = form.cleaned_data.get('amount'),
				image = form.cleaned_data.get('image'),
			)
			account.amount += int(form.cleaned_data.get('amount'))
			account.save()
			self.request.session['is_saved'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'cargo':
			account = form.cleaned_data.get('account')
			shipment = form.cleaned_data.get('shipment')
			SocioMovement.objects.create(
				socio = self.request.user,
			  account = form.cleaned_data.get('account'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				shipment = shipment,
				kind_charge = form.cleaned_data.get('kind_charge'),
				charge = form.cleaned_data['charge'],
				description = form.cleaned_data.get('description'),
				amount = form.cleaned_data.get('amount'),
				type_change = form.cleaned_data.get('type_change'),
				image = form.cleaned_data.get('image'),
			)
			if form.cleaned_data.get('account').currency == 'mxn':
				dolar_amount = int(form.cleaned_data.get('amount')) / form.cleaned_data.get('type_change')
				dolar_amount = "%.2f" % dolar_amount
				if shipment:
					# cargo directo
					shipment.saldo += float(dolar_amount)
					shipment.save()
				else:
					# cargo indirecto
					shipments = Shipment.objects.filter(saldo__gt = 0)
					amount_for_each_shipment = float(dolar_amount) / shipments.count()
					for shipment in shipments:
						shipment.saldo += amount_for_each_shipment
						shipment.save()
			if form.cleaned_data.get('account').currency == 'usd':
				if shipment:
					# cargo directo
					shipment.saldo += int(form.cleaned_data.get('amount'))
					shipment.save()
				else:
					# cargo indirecto
					shipments = Shipment.objects.filter(saldo__gt = 0)
					amount_for_each_shipment = int(form.cleaned_data.get('amount')) / shipments.count()
					for shipment in shipments:
						shipment.saldo += amount_for_each_shipment
						shipment.save()
			account.amount -= int(form.cleaned_data.get('amount'))
			account.save()
			self.request.session['is_saved'] = True
		return super(CreateMovementView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if request.user.kind == "socio":
				return super(CreateMovementView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect(reverse('stores:dashboard'))
		else:
			return redirect(reverse('main:home'))


class DetailMovementView(TemplateView):

	template_name = 'users/socio_detail_movement.html'

	def post(self, request, *args, **kwargs):
		form = UpdateImage(request.POST, request.FILES)
		movement = get_object_or_404(SocioMovement, pk = kwargs['id'])
		if form.is_valid():
			movement.image = request.FILES['image']
			movement.save()
			return render(request, 'users/socio_detail_movement.html', {"movement" : movement, "form" : UpdateImage()})
		else:
			return render(request, 'users/socio_detail_movement.html', {"error" : True, "movement" : movement, "form" : UpdateImage()});


	def get_context_data(self, **kwargs):
		context = super(DetailMovementView, self).get_context_data(**kwargs)
		context['movement'] = get_object_or_404(SocioMovement, pk = kwargs['id'])
		context['form'] = UpdateImage()
		return context

class NotificationView(TemplateView):

	template_name = 'users/socios_notification.html'

	def get_context_data(self, **kwargs):
		context = super(NotificationView, self).get_context_data(**kwargs)
		notification = get_object_or_404(Notification, id = kwargs['id'])
		notification.viewed = True
		notification.save()
		print(notification)
		context['notification'] = notification
		return context

	def post(self, request, *args, **kwargs):
		notification = get_object_or_404(Notification, id = kwargs['id'])
		approved = False
		no_approved = False
		if 'approved' in request.POST:
			# APPROVED
			notification.store_movement.approved = True
			notification.store_movement.waiting = False
			approved = True
			if notification.user.kind == 'almacen':
				# Verificar si quien envia la notificacion es un almance
				# Sumar al CAPITAL USD EN SOCIOS
				account_dolar = Account.objects.get(currency__iexact='usd')
				account_dolar.amount += notification.store_movement.amount
				account_dolar.save()
				# Restar a Embarques
		if 'no_approved' in request.POST:
			# NO APPROVED
			notification.store_movement.waiting = False
			no_approved = True
		notification.store_movement.save()
		ctx = {'notification' : notification, 'approved': approved, 'no_approved': no_approved}
		return render(request, 'users/socios_notification.html', ctx)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if request.user.kind == "socio":
				return super(NotificationView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect(reverse('stores:dashboard'))
		else:
			return redirect(reverse('main:home'))

class ViewedNotification(View):

	def get(self, request, *args, **kwargs):
		notification = get_object_or_404(Notification, id = kwargs['id'])
		notification.viewed = True
		notification.save()
		return JsonResponse({ 'success' : True })

class SocioExportDashboard(View):

	def get(self, request, *args, **kwargs):
		dolares = SocioMovement.objects.filter(account__currency__iexact='usd').order_by('-created_at')
		pesos = SocioMovement.objects.filter(account__currency__iexact='mxn').order_by('-created_at')
		
		result_list = list(chain(dolares, pesos))

		dataset = MovementResource().export(result_list)
		response = HttpResponse(dataset.csv, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="movimientos.csv"'
		return response
