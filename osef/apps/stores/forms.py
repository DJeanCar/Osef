from django import forms
from apps.shipments.models import Shipment, Charge, KindCharge
from apps.stores.models import KindMovement, Movement

class CreateMovForm(forms.Form):

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(CreateMovForm, self).__init__(*args, **kwargs)
		self.fields['shipment'] = forms.ModelChoiceField(
			required = False,
			queryset = Shipment.objects.filter(store = self.user, amount__gt = 0),
			empty_label="Selecciona un embarque"
		)

	_KIND_CHARGE = (
		('', 'Tipo de cargo'),
		('directo', 'Directo'),
		('indirecto', 'Indirecto')
	)

	kind_mov = forms.ModelChoiceField(
			required=False, 
			queryset=KindMovement.objects.filter(store = True),
			empty_label="Tipo de movimiento",
			to_field_name="name",
			widget=forms.Select(attrs={
				'id' : 'mov',
				'class' : 'input__margin'
			}))
	kind_charge = forms.ModelChoiceField(
			required=False,
			queryset=KindCharge.objects.all(), 
			empty_label="Selecciona un tipo de cargo",
			to_field_name="name",
			widget=forms.Select(attrs={
			'id' : 'kind-mov',
			'class' : 'input__margin'
		}))
	charge = forms.ModelChoiceField(
			required=False, 
			queryset=Charge.objects.all(), 
			empty_label="Selecciona un cargo",
			to_field_name="id",
			widget=forms.Select(attrs={
			'id' : 'kind-charge',
			'class' : 'input__margin'
		}))
	image = forms.ImageField(
			required=False,
		)
	description = forms.CharField(required=False, widget=forms.Textarea(attrs={
			'placeholder' : 'Descripción',
			'class' : 'materialize-textarea input__margin'
		}))
	amount = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder' : 'Cantidad',
			'type' : 'number',
			'class' : 'validate input__margin'
		}))

	def validateAmount(self):
		if self.cleaned_data.get('amount'):	
			if not self.cleaned_data['amount'].isdigit():
				self.add_error('amount', 'Este campo solo puede contener números')
			else:
				if self.cleaned_data['shipment']:
					if self.cleaned_data['shipment'].saldo < int(self.cleaned_data['amount']):
						self.add_error('amount', 'El embarque no tiene suficiente saldo')
		else:
			self.add_error('amount', 'Este campo es obligatorio')

	def clean(self):
		data = self.cleaned_data
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
						if not data.get('charge'):
							self.add_error('charge', 'Este campo es obligatorio')
						if not data['image']:
							self.add_error('image', 'Este campo es obligatorio')
					if data['kind_charge'].name.lower() == 'indirecto':
						if not data['description']:
							self.add_error('description', 'Este campo es obligatorio')
						if not data.get('charge'):
							self.add_error('charge', 'Este campo es obligatorio')
						else:
							if not data.get('image'):
								self.add_error('image', 'Este campo es obligatorio')
					self.validateAmount()
			if self.data['kind_mov'].lower() == 'abono':
				if not data['image']:
					self.add_error('image', 'Este campo es obligatorio')
				if not data['shipment']:
					self.add_error('shipment', 'Este campo es obligatorio')
				elif not data['description']:
					self.add_error('description', 'Este campo es obligatorio')
				elif not data['amount']:
					self.add_error('amount', 'Este campo es obligatorio')
				else:
					self.validateAmount()

