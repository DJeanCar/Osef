from django import forms
from apps.shipments.models import Shipment

class CreateMovForm(forms.Form):

	_KIND = (
		('-', 'Tipo de movimiento'),
		('cargo', 'Cargo'),
		('abono', 'Abono')
	)
	_CHARGE = (
		('-', 'Tipo de cargo'),
		('directo', 'Directo'),
		('indirecto', 'Indirecto')
	)

	kind_mov = forms.ChoiceField(choices=_KIND, widget=forms.Select(attrs={
			'id' : 'mov'
		}))
	kind_charge = forms.ChoiceField(choices=_CHARGE, widget=forms.Select(attrs={
			'id' : 'kind-mov'
		}))
	shipment = forms.ModelChoiceField(
			queryset = Shipment.objects.filter(amount__gt = 0),
			empty_label="Selecciona un embarque"
		)
	description = forms.CharField(widget=forms.Textarea(attrs={
			'placeholder' : 'Descripción',
			'class' : 'materialize-textarea'
		}))
	amount = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder' : 'Cantidad'
		}))
