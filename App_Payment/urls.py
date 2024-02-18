from django.urls import path
from App_Payment.views import *

app_name = 'App_Payment'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('pay/', payment, name='payment'),
    path('status/', complete, name='complete'),
    path('purchesed/<val_id>/<tran_id>/', purchesed, name='purchesed'),
    path('remove/<pk>/', remove_coupon, name='remove_coupon'),
]
