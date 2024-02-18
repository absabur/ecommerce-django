from django.db import models
from django.conf import settings

from App_Shop.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    coupon = models.CharField(max_length=100, default='')
    discount = models.IntegerField(default=0)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity} X {self.item}"
    
    def get_total(self):
        total = self.quantity * self.item.price
        return format(total, '0.2f')
    
class Order(models.Model):
    orderItems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    
    def get_totals(self):
        total = 0
        for order_item in self.orderItems.all():
            total += float(order_item.get_total())
        return total

