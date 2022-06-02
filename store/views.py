from django.shortcuts import get_object_or_404, render

from .models import Category, Product

"""Function showing all products from the store"""
def all_products(request):
	products = Product.objects.all()
	return render(request, "store/main.html", {"products": products})


"""Function showing all categories of products from the store"""
def category_list(request, category_slug):
	category = get_object_or_404(Category, slug=category_slug)
	products = Product.objects.filter(category=category)
	return render(request, 'store/category.html', {'category': category, 'products': products})


"""Function showing detail of one of product from the store"""
def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug, is_active=True)
	return render(request, 'store/details.html', {'product': product})


def our_blog(request):
	return render(request, 'store/blog.html')


def stationary_stores(request):
	return render(request, 'store/stationary_stores.html')
