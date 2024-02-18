from django.urls import path
from App_Shop.views import *

app_name = 'App_Shop'

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('product/<pk>/', ProductDetail, name="product_detail"),
    path('store-page/<pk>/', store_page, name="store_page"),
]