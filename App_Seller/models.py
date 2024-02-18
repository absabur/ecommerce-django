from django.db import models
from App_Auth.models import User
from App_Order.models import Order
import datetime

# Create your models here.
    
class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    shop_name = models.CharField(max_length=50)
    shop_address = models.CharField(max_length=264)
    shop_category = models.CharField(max_length=50)
    seller_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.shop_name
    
    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


class Coupon(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon')
    code = models.CharField(max_length=100)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=datetime.datetime.now())
    expiry_date = models.DateTimeField()
    
    def __str__(self):
        return self.code



class Order_seller(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sent_from_seller = models.BooleanField(default=False)
    