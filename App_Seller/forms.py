from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from App_Seller.models import *
from App_Shop.models import *


        
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('email', 'password1', 'password2')
    

class SellerProfileForm(ModelForm):
    class Meta:
        model = SellerProfile
        exclude = ('user',)
        
        
class Create_Product_Form(ModelForm):
    class Meta:
        model = Product
        exclude = ('created_by',)
        
        
        
class Create_Coupon_From(ModelForm):
    class Meta:
        model = Coupon
        exclude = ('seller',)
        labels = {
            'discount': 'Discount percentage',
        }
        widgets = {
            'discount': forms.TextInput(attrs={'placeholder': '10'}),
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'expiry_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
        
        
        
class Create_Category_Form(ModelForm):
    class Meta:
        model = Category
        fields = ('title',)