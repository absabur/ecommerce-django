from django.db import models
from App_Auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'
        


class Product(models.Model):
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=264)
    mainimage = models.ImageField(upload_to='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    description = models.TextField(max_length=1000, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated_at','name']
    