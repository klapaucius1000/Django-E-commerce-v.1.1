from importlib import import_module

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings

from store.models import Categories, Products
from store.views import all_products


class TestVievResponse(TestCase):
	def setUp(self):
		self.c = Client()
		User.objects.create(username='admin')
		Categories.objects.create(name='django1', slug='django1')
		Products.objects.create(category_id=1, title='django', slug='django1', created_by_id=1,
		                                     price='1.11', product_pic='django')


	def test_url_allowed_hosts(self):
		'''
		Testujemy dopuszczalny adres strony
		'''
		response = self.c.get('/', HTTP_HOST='sample.com')
		self.assertEqual(response.status_code, 400)
		response = self.c.get('/', HTTP_HOST='predatoryplantsshop.com')
		self.assertEqual(response.status_code, 200)



	def test_homepage_url(self):
		'''
		Testujemy status RESPONSE strony główny
		'''
		response = self.c.get('/')
		self.assertEqual(response.status_code, 200)

	def test_product_list_url(self):
		"""
		Test category response status
		"""
		response = self.c.get(
			reverse('store:category_list', args=['django']))
		self.assertEqual(response.status_code, 200)

	def test_products_detail_url(self):
		''' Sprawdzamy czy nasze Reverse RESPONSE W PRODUCTS działa poprawnie'''
		response = self.c.get(reverse('store:product_detail', args=['django1']))
		self.assertEqual(response.status_code, 200)

	def test_categories_detail_url(self):
		''' Sprawdzamy czy nasze Reverse RESPONSE W CATEGORIES działa poprawnie'''
		response = self.c.get(reverse('store:category_list', args=['django1']))
		self.assertEqual(response.status_code, 200)

	def test_homepage_html(self):
		request = HttpRequest()
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore()
		response = all_products(request)
		html = response.content.decode('utf8')
	#	print(html) ## -> Da nam dostęp w console do wszystkich plików HTML
		self.assertIn('<title>Main Page</title>', html)
		self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
		self.assertEqual(response.status_code, 200)



