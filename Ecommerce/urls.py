from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_Auth.urls')),
    path('', include('App_Shop.urls')),
    path('orders/', include('App_Order.urls')),
    path('payment/', include('App_Payment.urls')),
    path('seller/', include('App_Seller.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)