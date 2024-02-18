from django.urls import path
from App_Order.views import *

app_name = 'App_Order'

urlpatterns = [
    path('add/<pk>/', add_to_cart , name="add"),
    path('cart/', cart_view , name="cart"),
    path('remove-cart-item/<pk>/', remove_cart , name="remove_cart"),
    path('increase-item/<pk>/', increase_cart , name="increase"),
    path('decrease-item/<pk>/', decrease_cart, name="decrease"),
    path('orders/', orders_view, name="orders_view"),
]