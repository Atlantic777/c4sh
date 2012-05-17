from django import forms
from c4sh.backend import models as bmodels
from c4sh.desk import models as dmodels
from c4sh.preorder import models as pmodels
from django.contrib.auth.models import User

class AddCashierForm(forms.Form):
	username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
		error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
	first_name = forms.CharField(label="First name")
	last_name = forms.CharField(label="Last name")
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput
		)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1", "")
		password2 = self.cleaned_data["password2"]
		if password1 != password2:
			raise forms.ValidationError("The two password fields didn't match.")
		return password2

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("A user with that username already exists.")

class AddSessionForm(forms.ModelForm):
	class Meta:
		model = bmodels.CashdeskSession

class EditSessionForm(forms.ModelForm):
	class Meta:
		model = bmodels.CashdeskSession

