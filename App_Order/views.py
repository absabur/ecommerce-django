from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from App_Order.models import *
from App_Shop.models import *

# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "Cart Item quantity was increased")
            return redirect('App_Shop:home')
        else:
            order.orderItems.add(order_item[0])
            messages.info(request, "Item added to cart")
            return redirect('App_Shop:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        messages.info(request, "Item added to cart")
        return redirect('App_Shop:home')
    
    
@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased = False)
    orders = Order.objects.filter(user=request.user, ordered = False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart.html', {'order': order, 'carts':carts})
    else:
        messages.warning(request, "No item in cart")
        return redirect("App_Shop:home")
    
    


@login_required
def remove_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item):
            order_item = Cart.objects.filter(user=request.user, item=item, purchased=False)[0]
            order_item.delete()
            order.orderItems.remove(order_item)
            messages.info(request, "Item removed successfully")
            return redirect("App_Order:cart")         
        else:
            messages.warning(request, "This item not in cart")
            return redirect("App_Shop:home")
    else:
        messages.warning(request, "You don't have any active order")
        return redirect("App_Shop:home")
    
    
@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Quantity was increased")
                return redirect("App_Order:cart")
        else:
            messages.warning(request, f"No '{item.name}' in your cart")
            return redirect("App_Shop:home")
    else:
        messages.warning(request, "Unable to increase")
        return redirect("App_Shop:home")
    
    
@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Quantity was decreased")
                return redirect("App_Order:cart")
            else:
                messages.warning(request, "Quantity can't be less than 1")
                return redirect("App_Order:cart")
        else:
            messages.warning(request, f"No '{item.name}' in your cart")
            return redirect("App_Shop:home")
    else:
        messages.warning(request, "Unable to decrease")
        return redirect("App_Shop:home")
    
    

@login_required
def orders_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        if len(orders) == 0:
            messages.warning(request, "You don't have any orders")
            return redirect("App_Shop:home")
    except:
        messages.warning(request, "You don't have any orders")
        return redirect("App_Shop:home")
        
    return render(request, 'App_Order/order.html', context={"orders": orders})