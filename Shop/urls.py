import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('store.urls', namespace='store')),
	path('cart/', include('cart.urls', namespace='cart')),
	path('payment/', include('payment.urls', namespace='payment')),
	path('account/', include('account.urls', namespace='account')),
	path('orders/', include('orders.urls', namespace='orders')),
	path('__debug__/', include('debug_toolbar.urls')),
	path('api/schema/', SpectacularAPIView.as_view(), name='api_schema'),
	path('api/docs/', SpectacularSwaggerView.as_view(url_name='api_schema'),name='api_docs'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
