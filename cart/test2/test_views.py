from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Categories, Products

class TestCart(TestCase):
	def setUp(self):
		User.objects.create(username='admin')
		Categories.objects.create(name='django1', slug='django1')
		Products.objects.create(category_id=1, title='django', slug='django', created_by_id=1,
		                        price='1.11', product_pic='django')
		Categories.objects.create(name='django2', slug='django2')
		Products.objects.create(category_id=1, title='django2', slug='django2', created_by_id=1,
		                        price='1.11', product_pic='django')
		Categories.objects.create(name='django3', slug='django3')
		Products.objects.create(category_id=1, title='django3', slug='django3', created_by_id=1,
		                        price='1.11', product_pic='django')


		self.client.post(
			reverse('cart:cart_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
		self.client.post(
			reverse('cart:cart_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

	def test_cart_url(self):
		"""
		Sprawdzamy status strony G.
		"""
		response = self.client.get(reverse('cart:cart_summary'))
		self.assertEqual(response.status_code, 200)

	def test_cart_add(self):
		"""
		Test dodawania rzeczy do kosza
		"""
		response = self.client.post(
			reverse('cart:cart_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
		self.assertEqual(response.json(), {'qty': 4})
		response = self.client.post(
			reverse('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
		self.assertEqual(response.json(), {'qty': 3})

	def test_cart_delete(self):
		"""
		Test usuwania danych z koszyka
		"""
		response = self.client.post(
			reverse('cart:cart_delete'), {"productid": 2, "action": "post"}, xhr=True)
		self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

	def test_cart_update(self):
		"""
		Test uaktualniania koszyka
		"""
		response = self.client.post(
			reverse('cart:cart_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
		self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})