from django.urls import path
from App_Seller.views import *

app_name = 'App_Seller'

urlpatterns = [
    path('create-seller/', create_seller , name="create_seller"),
    path('seller-info/', fill_seller_info , name="fill_seller_info"),
    path('seller-dashboard/', seller_dashboard , name="seller_dashboard"),
    path('create-product/', create_product , name="create_product"),
    path('products/', seller_products , name="seller_products"),
    path('product-details/<pk>/', product_details , name="product_details"),
    path('edit-product/<pk>/', edit_product , name="edit_product"),
    path('delete_product/<pk>/', delete_product , name="delete_product"),
    path('create-coupon/', create_coupon , name="create_coupon"),
    path('coupons/', coupons , name="coupons"),
    path('update-coupon/<pk>/', update_coupon , name="update_coupon"),
    path('order/', order_for_seller , name="order_for_seller"),
    path('sent/<pk>/', sent , name="sent"),
    path('category-create/', create_category , name="create_category"),
    path('category/', all_category , name="all_category"),
    path('update-catgory/<pk>/', update_catgory , name="update_catgory"),
]