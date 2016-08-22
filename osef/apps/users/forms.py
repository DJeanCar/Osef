from django import forms
from .models import User


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