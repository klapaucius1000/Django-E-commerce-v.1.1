from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Categories, Products


class TestCategoriesModel(TestCase):
	def setUp(self):
		self.data1 = Categories.objects.create(name='django', slug='django')

	def test_categories_model_entry(self):
		data = self.data1
		self.assertTrue(isinstance(data, Categories))

	def test_categories_model_entry2(self):
		'''
		Sprawdzamy czy model jest poprawny przyrównując poprzednią nazwę do tej w teście
		'''
		data = self.data1
		self.assertEqual(str(data), 'django')



class TestPeoductsModel(TestCase):
	def setUp(self):
		Categories.objects.create(name='django', slug='django')
		User.objects.create(username='admin')
		self.data1 = Products.objects.create(category_id=1, title='django', slug='django', created_by_id=1,
		                                       price='1.11', product_pic='django')


	def test_products_model_entry(self):
		'''
		Testuje model PRODUCTS i pola atrybutów
		'''
		data = self.data1
		self.assertTrue(isinstance(data, Products))
		self.assertEqual(str(data), 'django')
