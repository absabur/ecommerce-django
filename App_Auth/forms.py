from django.forms import ModelForm
from App_Auth.models import *

from django.contrib.auth.forms import UserCreationForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('email', 'password1', 'password2')
