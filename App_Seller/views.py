from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from App_Seller.forms import *
from App_Order.models import *
# Create your views here.

#seller check

def create_seller(request):
    form = SignupForm()
    seller = True
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.role = 'seller'
            data.save()
            messages.success(request,"Seller Created Successfully!")
            return HttpResponseRedirect(reverse('App_Auth:login'))
    return render(request, 'App_Seller/signup.html', context={'form': form, 'seller': seller})


@login_required
def fill_seller_info(request):
    edit = False
    if (request.user.role != 'seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.seller.exists():
        form = SellerProfileForm()
        if request.method == 'POST':
            form = SellerProfileForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request,"Seller Info Created Successfully!")
                try:
                    if request.GET['next']:
                        return redirect(request.GET['next'])
                except Exception as e:
                    return redirect('App_Shop:home')
    else:
        edit = True
        seller = SellerProfile.objects.get(user=request.user)
        form = SellerProfileForm(instance=seller)
        print(seller)
        if request.method == 'POST':
            form = SellerProfileForm(request.POST, instance=seller)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request,"Seller Info Updated Successfully!")
                try:
                    if request.GET['next']:
                        return redirect(request.GET['next'])
                except Exception as e:
                    return redirect('App_Shop:home')
    return render(request, 'App_Seller/create_seller.html', context={'form': form, "edit": edit})


@login_required
def seller_dashboard(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    return render(request, 'App_Seller/dashboard.html')


@login_required
def create_product(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    form = Create_Product_Form()
    if (request.method == 'POST'):
        form = Create_Product_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.save()
            messages.success(request,"Product Created Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:seller_products'))
    return render(request, 'App_Seller/create_product.html', context={'form': form})


@login_required
def seller_products(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'App_Seller/products.html', context={'products': products})

@login_required
def product_details(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    product = Product.objects.filter(pk=pk, created_by=request.user)
    if not product.exists():
        messages.warning(request,"Product not found")
        return redirect("App_Seller:seller_products")
    return render(request, 'App_Seller/product_detail.html', context={'product': list(product)[0]})


@login_required
def edit_product(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    edit = True
    product = Product.objects.filter(pk=pk, created_by=request.user)
    if not product.exists():
        messages.warning(request,"Product not found")
        return redirect("App_Seller:seller_products")
    product = list(product)[0]
    form = Create_Product_Form(instance=product)
    if (request.method == 'POST'):
        form = Create_Product_Form(request.POST, request.FILES, instance=product)
        if form.is_valid():
            data = form.save()
            data.save()
            messages.success(request,"Product Updated Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:product_details', kwargs={'pk': pk}))
    return render(request, 'App_Seller/create_product.html', context={'form': form, "edit":edit})


@login_required
def delete_product(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    product = Product.objects.filter(pk=pk, created_by=request.user)
    if not product.exists():
        messages.warning(request,"Access denied")
        return redirect("App_Seller:seller_products")
    product = list(product)[0]
    product.delete()
    messages.success(request,"Product Deleted Successfully!")
    return HttpResponseRedirect(reverse('App_Seller:seller_products'))


@login_required
def create_coupon(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    form = Create_Coupon_From()
    if (request.method == 'POST'):
        form = Create_Coupon_From(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.seller = request.user
            data.save()
            messages.success(request,"Coupon Created Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:seller_dashboard'))
    return render(request, 'App_Seller/create_coupon.html', context={"form": form})


@login_required
def coupons(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    coupons = Coupon.objects.filter(seller=request.user)
    return render(request, 'App_Seller/coupons.html', context={"coupons": coupons})



@login_required
def update_coupon(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    edit = True
    coupon = Coupon.objects.filter(seller=request.user, pk=pk)
    if not coupon.exists():
        messages.warning(request,"Access denied")
        return redirect("App_Seller:coupons")
    coupon = list(coupon)[0]
    form = Create_Coupon_From(instance=coupon)
    if (request.method == 'POST'):
        form = Create_Coupon_From(request.POST, instance=coupon)
        if form.is_valid():
            data = form.save()
            data.save()
            messages.success(request,"Coupon Updated Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:seller_dashboard'))
    return render(request, 'App_Seller/create_coupon.html', context={"form": form, "edit": edit})


@login_required
def order_for_seller(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    All_order = []
    orders = Order.objects.filter(ordered=True)
    for order in orders:
        items = order.orderItems.all()
        seller_order = []
        for i in items:
            product = Product.objects.get(id=i.item.id)
            if product and product.created_by==request.user:
                item = {"product": product, "quantity": i.quantity}
                seller_order.append(item)
        Order_seller.objects.get_or_create(seller=request.user, order=order)
        order_item = Order_seller.objects.get(seller=request.user, order=order)
        All_order.append({"order_item":order_item, "seller_order":seller_order})
    return render(request, 'App_Seller/order.html', context={"order": All_order})



@login_required
def sent(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    order = Order_seller.objects.filter(pk=pk, seller=request.user)
    if not order.exists():
        messages.warning(request,"Access denied")
        return redirect("App_Seller:order_for_seller")
    order = list(order)[0]
    if (order.sent_from_seller):
        order.sent_from_seller = False
        order.save()
    else:
        order.sent_from_seller = True
        order.save()
    return HttpResponseRedirect(reverse('App_Seller:order_for_seller'))


@login_required
def create_category(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    form = Create_Category_Form()
    if request.method == 'POST':
        form = Create_Category_Form(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.save()
            messages.success(request,"Category Created Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:seller_dashboard'))
    return render(request, 'App_Seller/create_category.html',context={"form": form})
    
@login_required
def update_catgory(request, pk):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    category = Category.objects.get(pk=pk)
    edit = True
    form = Create_Category_Form(instance=category)
    if request.method == 'POST':
        form = Create_Category_Form(request.POST, instance=category)
        if form.is_valid():
            data = form.save()
            data.save()
            messages.success(request,"Category Updated Successfully!")
            return HttpResponseRedirect(reverse('App_Seller:seller_dashboard'))
    return render(request, 'App_Seller/create_category.html',context={"form": form, "edit": edit})
    


@login_required
def all_category(request):
    if (request.user.role!='seller'):
        messages.warning(request, "Only seller can access this page.")
        return HttpResponseRedirect(reverse('App_Shop:home'))
    if not request.user.profile.is_fully_filled():
        messages.warning(request,"Complete profile details first!")
        first = reverse("App_Auth:change_profile")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    seller_exists = SellerProfile.objects.filter(user=request.user)
    if not seller_exists:
        messages.warning(request,"Complete seller details first!")
        first = reverse("App_Seller:fill_seller_info")
        next = reverse("App_Seller:seller_dashboard")
        return redirect("{}?next={}".format(first, next))
    category = Category.objects.all()
    return render(request, 'App_Seller/category.html',context={"category": category})
    