from django.http.response import JsonResponse

from cart.cart import Cart
from .models import Order, OrderItem


def add(request):
	"""Creating new order, checking that this order exist, and later creating user order"""
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		user_id = request.user.id
		order_key = request.POST.get('order_key')
		carttotal = cart.get_total_price()
		if Order.objects.filter(order_key=order_key).exists():
			pass
		else:
			order = Order.objects.create(user_id=user_id, full_name='name', addres1='addres1', addres2='addres2',
			                             total_paid=carttotal, order_key=order_key)
			order_id = order.pk
			for item in cart:
				OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
				                         quantity=item['qty'])

			response = JsonResponse({'success': 'return_sth'})
			return response


def payment_confirmation(data):
	"""As above """
	Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
	"""Checking user orders via user id"""
	user_id = request.user.id
	orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
	return orders
