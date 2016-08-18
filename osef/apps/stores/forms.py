from django import forms
from apps.shipments.models import Shipment, Charge, KindCharge
from apps.stores.models import KindMovement, Movement

class CreateMovForm(forms.Form):

	_KIND_CHARGE = (
		('', 'Tipo de cargo'),
		('directo', 'Directo'),
		('indirecto', 'Indirecto')
	)

	kind_mov = forms.ModelChoiceField(
			required=False, 
			queryset=KindMovement.objects.all(),
			empty_label="Tipo de movimiento",
			to_field_name="name",
			widget=forms.Select(attrs={
				'id' : 'mov'
			}))
	kind_charge = forms.ModelChoiceField(
			required=False,
			queryset=KindCharge.objects.all(), 
			empty_label="Selecciona un tipo de cargo",
			to_field_name="name",
			widget=forms.Select(attrs={
			'id' : 'kind-mov'
		}))
	charge = forms.ModelChoiceField(
			required=False, 
			queryset=Charge.objects.all(), 
			empty_label="Selecciona un cargo",
			to_field_name="id",
			widget=forms.Select(attrs={
			'id' : 'kind-charge'
		}))
	shipment = forms.ModelChoiceField(
			required = False,
			queryset = Shipment.objects.filter(amount__gt = 0),
			empty_label="Selecciona un embarque"
		)
	description = forms.CharField(required=False, widget=forms.Textarea(attrs={
			'placeholder' : 'Descripción',
			'class' : 'materialize-textarea'
		}))
	amount = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder' : 'Cantidad',
			'type' : 'number'
		}))

	def clean(self):
		data = self.cleaned_data
		print(self.cleaned_data)
		print(data.get('charge'))
		if not data['kind_mov']:
			self.add_error('kind_mov', 'Este campo es obligatorio')
		else:
			if self.data['kind_mov'].lower() == 'cargo':
				if not data['kind_charge']:
					self.add_error('kind_charge', 'Este campo es obligatorio')
				else:
					if data['kind_charge'].name.lower() == 'directo':
						if not data['shipment']:
							self.add_error('shipment', 'Este campo es obligatorio')
						if not data['description']:
							self.add_error('description', 'Este campo es obligatorio')
						if not data['amount']:
							self.add_error('amount', 'Este campo es obligatorio')
						if not data.get('charge'):
							self.add_error('charge', 'Este campo es obligatorio')
					if data['kind_charge'].name.lower() == 'indirecto':
						if not data['description']:
							self.add_error('description', 'Este campo es obligatorio')
						if not data['amount']:
							self.add_error('amount', 'Este campo es obligatorio')
						if not data.get('charge'):
							self.add_error('charge', 'Este campo es obligatorio')
			if self.data['kind_mov'].lower() == 'abono':
				if not data['shipment']:
					self.add_error('shipment', 'Este campo es obligatorio')
				if not data['description']:
					self.add_error('description', 'Este campo es obligatorio')
				if not data['amount']:
					self.add_error('amount', 'Este campo es obligatorio')

