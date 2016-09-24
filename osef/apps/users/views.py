from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.shipments.models import Shipment
from apps.stores.models import SocioMovement
from .models import Account
from .forms import EmailForm, CreateMovForm

class DashboardView(LoginRequiredMixin, TemplateView):

	template_name = 'users/dashboard.html'
	login_url = '/'

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
			Shipment.objects.create(
					store = form.cleaned_data['store'],
					name = form.cleaned_data['name'],
					amount = form.cleaned_data['amount_shipment']
				)
			self.request.session['is_saved_shipment'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'retiro':
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
			self.request.session['is_saved'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'abono':
			SocioMovement.objects.create(
				socio = self.request.user,
			  account = form.cleaned_data.get('account'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				kind_abono = form.cleaned_data.get('kind_abono'),
				description = form.cleaned_data.get('description'),
				amount = form.cleaned_data.get('amount'),
				image = form.cleaned_data.get('image'),
			)
			self.request.session['is_saved'] = True
		if form.cleaned_data['kind_mov'].name.lower() == 'cargo':
			SocioMovement.objects.create(
				socio = self.request.user,
			  account = form.cleaned_data.get('account'),
				kind_mov = form.cleaned_data.get('kind_mov'),
				shipment = form.cleaned_data.get('shipment'),
				kind_charge = form.cleaned_data.get('kind_charge'),
				charge = form.cleaned_data['charge'],
				description = form.cleaned_data.get('description'),
				amount = form.cleaned_data.get('amount'),
				image = form.cleaned_data.get('image'),
			)
			self.request.session['is_saved'] = True
		return super(CreateMovementView, self).form_valid(form)


