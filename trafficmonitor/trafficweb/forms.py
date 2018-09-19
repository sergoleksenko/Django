from django import forms
from django.core.exceptions import ValidationError


class CompanyForm(forms.Form):
	name = forms.CharField(max_length=100)
	quota = forms.IntegerField(help_text='Monthly transfer quota (TB)')

	def clean_quota(self):
		data = self.cleaned_data['quota']
		if data < 0:
			raise ValidationError('quota should not be negative')

		return data


class EmployeeForm(forms.Form):
	company = forms.ChoiceField()
	name = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)

	def clean_company(self):
		data = self.cleaned_data['company']
		if data == '0':
			raise ValidationError('you have to choice a company')

		return data
