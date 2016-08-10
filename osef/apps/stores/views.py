from django.shortcuts import render
from django.views.generic import TemplateView

class StoreDashboard(TemplateView):

	template_name = 'stores/dashboard.html'
	