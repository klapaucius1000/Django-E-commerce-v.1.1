from store.models import Product
from django.conf import settings
from decimal import Decimal


class Cart():
	"""
	Our base CART Class.Provides some default class behavior that can be inherited as needed or replaced.
	"""

	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('session_key')
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}
		self.cart = cart

	def add(self, product, qty):
		"""		adding refresh our cart during sessions """
		product_id = str(product.id)

		if product_id in self.cart:
			self.cart[product_id]['qty'] += qty
		else:
			self.cart[product_id] = {'price': str(product.normal_price), 'qty': qty}

		self.save()

	def __iter__(self):
		"""
		Gather data from product_id from session to query DB and return products
		"""
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()

		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['qty']
			yield item

	def __len__(self):
		"""
		take the data from the cart and keep the number QTY
		"""

		return sum(item['qty'] for item in self.cart.values())

	def get_subtotal_price(self):
		"""Shows the price before shipping costs"""
		return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

	def get_total_price(self):
		"""Shows the price after shipping costs"""
		before_delivery = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

		if before_delivery == 0:
			shipping = Decimal(0.00)
		else:
			shipping = Decimal(14.49)

		total = before_delivery + Decimal(shipping)
		totalrounded = round(total, 2)
		return totalrounded

	def delete(self, product):
		"""Deleting data from session"""
		product_id = str(product)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def update(self, product, qty):
		"""Updating data from session"""

		product_id = str(product)
		if product_id in self.cart:
			self.cart[product_id]['qty'] += qty
		self.save()

	def save(self):
		"""Saving data from session"""
		self.session.modified = True

	def clear(self):
		"""Clearing data from session"""
		del self.session[settings.CART_SESSION_ID]
		self.save()
