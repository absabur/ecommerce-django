from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from App_Payment.forms import BillingAddressForm
from App_Payment.models import BillingAddress
from App_Order.models import Order, Cart
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from App_Seller.models import *

#payment methods
from sslcommerz_lib import SSLCOMMERZ

# Create your views here.
@login_required
def checkout(request):
    discount_total = 0
    restart_cart = Cart.objects.filter(user=request.user, purchased = False)
    for item in restart_cart:
        coupons = Coupon.objects.filter(seller=item.item.created_by)
        expired = True
        for coupon in coupons:
            if item.coupon == coupon.code:
                date_time_start = datetime.datetime.strptime(str(coupon.start_date)[:19], "%Y-%m-%d %H:%M:%S")
                date_time_end = datetime.datetime.strptime(str(coupon.expiry_date)[:19], "%Y-%m-%d %H:%M:%S")
                if coupon.active and date_time_start < datetime.datetime.now():
                    if date_time_end > datetime.datetime.now():
                        expired = False
        if expired:
            item.coupon = ""
            item.discount = 0
            item.save()
        if item.discount == 0:
            discount_total += item.quantity * item.item.price
        discount_total += item.discount
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingAddressForm(instance=saved_address)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    orders = order_qs[0].orderItems.all()
    final_orders = []
    for order in orders:
        coupons = Coupon.objects.filter(seller=order.item.created_by)
        filtered_coupon = []
        for coupon in coupons:
            date_time_start = datetime.datetime.strptime(str(coupon.start_date)[:19], "%Y-%m-%d %H:%M:%S")
            date_time_end = datetime.datetime.strptime(str(coupon.expiry_date)[:19], "%Y-%m-%d %H:%M:%S")
            if coupon.active and date_time_start < datetime.datetime.now():
                if date_time_end > datetime.datetime.now():
                    filtered_coupon.append(coupon)
        final_orders.append({'order': order, 'coupon': filtered_coupon})
    order_total = order_qs[0].get_totals()
    if request.method == 'POST':
        if 'custom_form_submit' in request.POST:
            code = request.POST["code"].strip()
            cart = Cart.objects.get(id=request.POST['id'])
            coupons = Coupon.objects.filter(seller=cart.item.created_by)
            for coupon in coupons:
                if coupon.code == code:
                    cart.coupon = code
                    price = cart.item.price * cart.quantity
                    cart.discount = price - (price * coupon.discount / 100)
                    cart.save()
                    messages.success(request, "Coupon added successfully!")
                    return redirect('App_Payment:checkout')
            messages.warning(request, "Invalid Coupon!")        
            return redirect('App_Payment:checkout')
        else:
            form = BillingAddressForm(request.POST, instance=saved_address)
            if form.is_valid():
                form.save()
    return render(request, 'App_Payment/checkout.html', context={"address": saved_address,"form": form, "orders": final_orders, "total": order_total, "final_price": discount_total, "discount": order_total - discount_total})


@login_required
def remove_coupon(request, pk):
    item = Cart.objects.get(pk=pk)
    item.coupon = ""
    item.discount = 0
    item.save()
    messages.info(request, "Coupon Removed")        
    return redirect('App_Payment:checkout')


@login_required
def payment(request):
    discount_total = 0
    restart_cart = Cart.objects.filter(user=request.user, purchased = False)
    for item in restart_cart:
        coupons = Coupon.objects.filter(seller=item.item.created_by)
        expired = True
        for coupon in coupons:
            if item.coupon == coupon.code:
                date_time_start = datetime.datetime.strptime(str(coupon.start_date)[:19], "%Y-%m-%d %H:%M:%S")
                date_time_end = datetime.datetime.strptime(str(coupon.expiry_date)[:19], "%Y-%m-%d %H:%M:%S")
                if coupon.active and date_time_start < datetime.datetime.now():
                    if date_time_end > datetime.datetime.now():
                        expired = False
        if expired:
            item.coupon = ""
            item.discount = 0
            item.save()
        if item.discount == 0:
            discount_total += item.quantity * item.item.price
        discount_total += item.discount
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.warning(request,"Complete shipping address")
        return redirect("App_Payment:checkout")
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    store_id = 'abs65c269ecb8d55'
    store_pass = 'abs65c269ecb8d55@ssl'
    settings = { 'store_id': store_id, 'store_pass': store_pass, 'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)
    
    url = request.build_absolute_uri(reverse('App_Payment:complete'))
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    orders = order_qs[0].orderItems.all()
    order_count = order_qs[0].orderItems.count()
    order_total = discount_total
    
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = order_qs[0].pk
    post_body['success_url'] = url
    post_body['fail_url'] = url
    post_body['cancel_url'] = url
    post_body['emi_option'] = 0
    post_body['ship_postcode'] = saved_address.zipcode
    post_body['cus_add1'] = request.user.profile.address_1
    post_body['cus_city'] = request.user.profile.city
    post_body['cus_name'] = request.user.profile.full_name
    post_body['cus_country'] = request.user.profile.counrty
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = request.user.profile.phone
    post_body['ship_name'] = request.user.profile.full_name
    post_body['ship_add1'] = saved_address.address
    post_body['ship_city'] = saved_address.city
    post_body['ship_country'] = saved_address.country
    post_body['shipping_method'] = "Courier"
    post_body['multi_card_name'] = "NA"
    post_body['num_of_item'] = order_count
    post_body['product_name'] = orders
    post_body['product_category'] = "Multiple Category"
    post_body['product_profile'] = "general"
    
    response = sslcommez.createSession(post_body)
    pay_url = response['GatewayPageURL']
    return redirect(pay_url)

@csrf_exempt
def complete(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            messages.success(request, "Payment successful")
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            return HttpResponseRedirect(reverse('App_Payment:purchesed', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request, "Payment failed! Please Try Again")
    return render(request, 'App_Payment/complete.html')


@login_required
def purchesed(request, val_id, tran_id):
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered = False)    
    order = order_qs[0]
    order.ordered = True
    order.paymentId = val_id
    order.orderId = tran_id
    order.save()
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('App_Order:orders_view'))