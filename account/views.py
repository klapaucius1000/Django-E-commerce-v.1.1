from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from store.models import Product
from .models import Customer, Address
from .token import account_activation_token

from orders.views import user_orders


@login_required
def dashboard(request):
	orders = user_orders(request)
	return render(request, 'account/user/dashboard.html', {'orders': orders})


@login_required
def edit_details(request):
	if request.method == "POST":
		user_form = UserEditForm(instance=request.user, data=request.POST)

		if user_form.is_valid():
			user_form.save()
	else:
		user_form = UserEditForm(instance=request.user)

	return render(request, 'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
	user = Customer.objects.get(user_name=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('account:delete_confirmation')


def account_register(request):
	if request.method == 'POST':
		registerForm = RegistrationForm(request.POST)
		if registerForm.is_valid():
			user = registerForm.save(commit=False)
			user.email = registerForm.cleaned_data['email']
			user.set_password(registerForm.cleaned_data['password'])
			user.is_active = False
			user.save()
			# EMAIL CONF
			current_site = get_current_site(request)
			subject = 'Please, active your account'
			message = render_to_string('account/registration/account_activation.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject=subject, message=message)
			return render(request, 'account/registration/registration_email_confirm.html', {'form': registerForm})
	else:
		registerForm = RegistrationForm()
	return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = Customer.objects.get(pk=uid)
	except():
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('account:dashboard')
	else:
		return render(request, 'account/registration/activation_failed.html')


# ADRESSES


@login_required
def view_address(request):
	addresses = Address.objects.filter(customer=request.user)
	return render(request, 'account/user/addresses.html', {"addresses": addresses})


@login_required
def add_address(request):
	if request.method == "POST":
		address_form = UserAddressForm(data=request.POST)
		if address_form.is_valid():
			address_form = address_form.save(commit=False)
			address_form.customer = request.user
			address_form.save()
			return HttpResponseRedirect(reverse("account:addresses"))
	else:
		address_form = UserAddressForm()
	return render(request, "account/user/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
	if request.method == "POST":
		address = Address.objects.get(pk=id, customer=request.user)
		address_form = UserAddressForm(instance=address, data=request.POST)
		if address_form.is_valid():
			address_form.save()
			return HttpResponseRedirect(reverse("account:addresses"))
	else:
		address = Address.objects.get(pk=id, customer=request.user)
		address_form = UserAddressForm(instance=address)
	return render(request, "account/user/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
	address = Address.objects.filter(pk=id, customer=request.user).delete()
	return redirect("account:addresses")


@login_required
def set_default(request, id):
	Address.objects.filter(customer=request.user, default=True).update(default=False)
	Address.objects.filter(pk=id, customer=request.user).update(default=True)
	return redirect("account:addresses")


# FAVOURITES


@login_required
def favourites(request):
	products = Product.objects.filter(users_favourites=request.user)
	return render(request, "account/user/your_favourites.html", {"users_favourites": products})


@login_required
def add_to_favourites(request, id):
	product = get_object_or_404(Product, id=id)
	if product.users_favourites.filter(id=request.user.id).exists():
		product.users_favourites.remove(request.user)
		messages.success(request, "You remove " + product.title + " from your Favourites")
	else:
		product.users_favourites.add(request.user)
		messages.success(request, "You add " + product.title + " to your Favourites")
	return HttpResponseRedirect(request.META['HTTP_REFERER'])