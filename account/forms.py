from django import forms
from .models import Customer, Address
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


class UserLoginForm(AuthenticationForm):
	"""Class to user login"""

	username = forms.CharField(widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))

	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'login-pwd', }))


class RegistrationForm(forms.ModelForm):
	"""Class to user register"""
	user_name = forms.CharField(label='Enter your username', min_length=3, max_length=40, help_text='Required')
	email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Email is mandatory'})
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat your password', widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ('user_name', 'email')

	def clean_username(self):
		"""Function to cleaning username"""
		user_name = self.cleaned_data['user_name'].lower()
		r = Customer.objects.filter(user_name=user_name)
		if r.count():
			raise forms.ValidationError("Sorry, this username already exists")
		return user_name

	def clean_password2(self):
		"""Function to checking similarity passwords"""
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('These passwords do not match.')
		return cd['password2']

	def clean_email(self):
		"""Function to cleaning pass"""
		email = self.cleaned_data['email']
		if Customer.objects.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another Email adress. That is already taken')
		return email

	def __init__(self, *args, **kwargs):
		"""Initializing func"""
		super().__init__(*args, **kwargs)
		self.fields['user_name'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'Username'})
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
		self.fields['password'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'Password'})
		self.fields['password2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Repeat Password'})


class PwdResetForm(PasswordResetForm):
	"""Class to resset pass"""
	email = forms.EmailField(max_length=254, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

	def clean_email(self):
		"""Cleaning email"""
		email = self.cleaned_data['email']
		reset = Customer.objects.filter(email=email)
		if not reset:
			raise forms.ValidationError(
				'Unfortunately, we have not found such an address in our database.')
		return email


class PwdResetConfirmForm(SetPasswordForm):
	"""Class confirming the change of the pass"""
	new_password1 = forms.CharField(
		label='New password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
	new_password2 = forms.CharField(
		label='Repeat password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
	"""Class editing user data"""
	email = forms.EmailField(
		label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

	user_name = forms.CharField(
		label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname',
			       'readonly': 'readonly'}))

	first_name = forms.CharField(
		label='Username', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

	class Meta:
		model = Customer
		fields = ('email', 'user_name', 'first_name',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['user_name'].required = True
		self.fields['email'].required = True


class UserAddressForm(forms.ModelForm):
	"""Class editing user address"""
	class Meta:
		model = Address
		fields = ['full_name', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'zipcode']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['full_name'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'Your full name here'}
		)
		self.fields['phone_number'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'Your phone here'})
		self.fields['address_line_1'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'Address line 1'}
		)
		self.fields['address_line_2'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'Address line 2'}
		)
		self.fields['city'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'The place where you live'}
		)
		self.fields['zipcode'].widget.attrs.update(
			{'class': 'form-control mb-2 account-form', 'placeholder': 'Zip code of your city'}
		)
