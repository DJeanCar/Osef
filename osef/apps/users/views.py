from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):

	template_name = 'users/dashboard.html'
	login_url = '/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.has_permission:
			return super(DashboardView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect(reverse('users:no_permission'))


class NoPermissionView(LoginRequiredMixin, TemplateView):

	template_name = 'users/no_permission.html'
	login_url = '/'


def LogOut(request):
	logout(request)
	return redirect(reverse('main:home'))