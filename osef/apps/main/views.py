from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

class HomeView(TemplateView):

	template_name = 'main/home.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect(reverse('users:dashboard'))
		else:
			return super(HomeView, self).dispatch(request, *args, **kwargs)