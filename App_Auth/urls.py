from django.urls import path
from App_Auth.views import *

app_name = 'App_Auth'

urlpatterns = [
    path('signup/', signup , name="signup"),
    path('login/', login_page , name="login"),
    path('logout/', logout_page , name="logout"),
    path('change-profile/', change_profile , name="change_profile"),
]