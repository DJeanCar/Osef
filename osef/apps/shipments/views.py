from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.core import serializers

from .models import Charge

class GetCargesAjax(View):

	def get(self, request, *args, **kwargs):
		charges = Charge.objects.filter(kind__name=request.GET['kind_charge'])
		return JsonResponse(serializers.serialize('json', charges), safe=False)
