from django import forms
from .models import User, Account
from apps.stores.models import KindMovement, Movement
from apps.shipments.models import Shipment, Charge, KindCharge, Abono


class EmailForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email',)
		widgets = {
			'email' : forms.TextInput(attrs={
					'type' : 'email',
					'placeholder' : 'Email'
				})
		}


class CreateMovForm(forms.Form):

  _KIND_CHARGE = (
    ('', 'Tipo de cargo'),
    ('directo', 'Directo'),
    ('indirecto', 'Indirecto')
  )
  _CURRENCY = (
    ('', 'Selecciona la cuenta'),
    ('usd', 'Dólares'),
    ('mxn', 'Pesos mexicanos'),
  )

  kind_mov = forms.ModelChoiceField(
      required=False, 
      queryset=KindMovement.objects.all(),
      empty_label="Tipo de movimiento",
      to_field_name="name",
      widget=forms.Select(attrs={
        'id' : 'mov',
        'class' : 'input__margin'
      }))
  kind_abono = forms.ModelChoiceField(
      required=False,
      queryset=Abono.objects.all(), 
      empty_label="Selecciona un tipo de abono",
      to_field_name="name",
      widget=forms.Select(attrs={
      'id' : 'kind-abono',
      'class' : 'input__margin'
    }))
  shipment = forms.ModelChoiceField(
      required=False,
      queryset=Shipment.objects.filter(amount__gt = 0),
      empty_label="Selecciona un embarque",
      to_field_name="name",
      widget=forms.Select(attrs={
      'id' : 'shipment',
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
  type_change = forms.DecimalField(
      required=False,
      widget=forms.NumberInput(attrs={
        'id' : 'type-change',
        'placeholder': 'Tipo de cambio: 20.4',
        'class' : 'input__margin'
        })
    )
  account = forms.ModelChoiceField(
      required=False, 
      queryset=Account.objects.all(),
      empty_label="Selecciona una Cuenta",
      to_field_name="currency",
      widget=forms.Select(attrs={
        'id' : 'currency',
        'class' : 'input__margin'
      }))
  description = forms.CharField(required=False, widget=forms.Textarea(attrs={
      'placeholder' : 'Descripción',
      'class' : 'materialize-textarea input__margin'
    }))
  amount = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
      'placeholder' : 'Cantidad',
      'type' : 'number',
      'class' : 'validate input__margin'
    }))

  # shipment
  store = forms.ModelChoiceField(
      required=False, 
      queryset=User.objects.filter(kind="almacen"),
      empty_label="Elegir Almancén",
      widget=forms.Select(attrs={
        'id' : 'store',
        'class' : 'input__margin',
      }))
  name = forms.CharField(required=False, widget=forms.TextInput(attrs={
      'placeholder' : 'Nombre',
      'type' : 'text',
      'class' : 'validate input__margin'
    }))
  amount_shipment = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
      'placeholder' : 'Cantidad',
      'type' : 'number',
      'class' : 'validate input__margin'
    }))

  # retiro
  socio = forms.ModelChoiceField(
      required=False, 
      queryset=User.objects.filter(kind="socio"),
      empty_label="Elegir Socio",
      widget=forms.Select(attrs={
        'id' : 'socio',
        'class' : 'input__margin',
      }))

  def validateAmount(self):
    if not self.cleaned_data['amount'].isdigit():
      self.add_error('amount', 'Este campo solo puede contener números')
    else:
      if self.cleaned_data['shipment'].saldo < int(self.cleaned_data['amount']):
        self.add_error('amount', 'El embarque no tiene suficiente saldo')

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
            if not data['amount']:
              self.add_error('amount', 'Este campo es obligatorio')
            else:
              if not data['amount'].isdigit():
                self.add_error('amount', 'Este campo solo puede contener números')
          if data['kind_charge'].name.lower() == 'indirecto':
            if not data['description']:
              self.add_error('description', 'Este campo es obligatorio')
            if not data.get('charge'):
              self.add_error('charge', 'Este campo es obligatorio')
            if not data['amount']:
              self.add_error('amount', 'Este campo es obligatorio')
            else:
              if not data['amount'].isdigit():
                self.add_error('amount', 'Este campo solo puede contener números')
          if not data['account']:
            self.add_error('account', 'Este campo es obligatorio')
          else:
            if data["account"].currency == "mxn":
              if not data['type_change']:
                self.add_error('type_change', 'Este campo solo puede contener números')
      if self.data['kind_mov'].lower() == 'abono':
        if not data['kind_abono']:
          self.add_error('kind_abono', 'Este campo es obligatorio')
        if not data['account']:
          self.add_error('account', 'Este campo es obligatorio')
        if not data['description']:
          self.add_error('description', 'Este campo es obligatorio')
        if not data['amount']:
          self.add_error('amount', 'Este campo es obligatorio')
        else:
          if not str(self.cleaned_data['amount']).isdigit():
            self.add_error('amount', 'Este campo solo puede contener números')
      if self.data['kind_mov'].lower() == 'embarque':
        if not data['store']:
          self.add_error('store', 'Este campo es obligatorio')
        if not data['name']:
          self.add_error('name', 'Este campo es obligatorio')
        if not data['amount_shipment']:
          self.add_error('amount_shipment', 'Este campo es obligatorio')
        else:
          account = Account.objects.get(currency="usd")
          if account.amount < int(data['amount_shipment']):
            self.add_error('amount_shipment', 'No tiene saldo sufiencie en su cuenta')
      if self.data['kind_mov'].lower() == 'retiro':
        if not data['socio']:
          self.add_error('socio', 'Este campo es obligatorio')
        if not data['account']:
          self.add_error('account', 'Este campo es obligatorio')
        if not data['description']:
          self.add_error('description', 'Este campo es obligatorio')
        if not data['amount']:
          self.add_error('amount', 'Este campo es obligatorio')
        else:
          if int(data['account'].amount < int(data['amount'])):
            self.add_error('amount', 'No tiene saldo sufiencie en su cuenta')
          if data.get('amount'):
            if not data.get('amount').isdigit():
              self.add_error('amount', 'Este campo solo puede contener números')


class UpdateImage(forms.Form):

  image = forms.ImageField(
      required=True,
    )

