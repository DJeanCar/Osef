from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EmailForm

class DashboardView(LoginRequiredMixin, TemplateView):

	template_name = 'users/dashboard.html'
	login_url = '/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.has_permission:
			return super(DashboardView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect(reverse('users:no_permission'))

class UserProfileView(LoginRequiredMixin, TemplateView):

    template_name = "users/profile.html"
    login_url = '/'

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

