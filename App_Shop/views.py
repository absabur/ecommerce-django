from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import datetime

from App_Seller.models import *

from App_Shop.models import *

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'
    

def ProductDetail(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user == product.created_by:
        return HttpResponseRedirect(reverse('App_Seller:product_details', kwargs={'pk': pk}))
    store = SellerProfile.objects.get(user=product.created_by)
    coupons = Coupon.objects.filter(seller=product.created_by)
    filtered_coupon = []
    for coupon in coupons:
        date_time_start = datetime.datetime.strptime(str(coupon.start_date)[:19], "%Y-%m-%d %H:%M:%S")
        date_time_end = datetime.datetime.strptime(str(coupon.expiry_date)[:19], "%Y-%m-%d %H:%M:%S")
        if coupon.active and date_time_start < datetime.datetime.now():
            if date_time_end > datetime.datetime.now():
                filtered_coupon.append(coupon)
    return render(request, 'App_Shop/product_detail.html', context={"product": product, "coupons": filtered_coupon, "store": store})


def store_page(request, pk):
    seller = User.objects.get(pk=pk)
    store = SellerProfile.objects.get(user=seller)
    products = Product.objects.filter(created_by=seller)
    coupons = Coupon.objects.filter(seller=seller)
    return render(request, 'App_Shop/store.html', context={"store": store, "products": products, "coupons": coupons, "id": pk})