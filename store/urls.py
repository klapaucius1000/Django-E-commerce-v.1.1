from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
	path('', views.all_products, name='all_products'),
	path('our_blog/', views.our_blog, name='our_blog'),
	path('/stationary_stores/', views.stationary_stores, name='stationary_stores'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),
	path('store/<slug:category_slug>/', views.category_list, name='category_list'),

]