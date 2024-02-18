from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from App_Auth.forms import *
from App_Auth.models import *

from django.contrib import messages

# Create your views here.
def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully!")
            return HttpResponseRedirect(reverse('App_Auth:login'))
    return render(request,'App_Auth/signup.html', context={'form': form})

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    if request.GET['next']:
                        return redirect(request.GET['next'])
                except Exception as e:
                    messages.success(request,"Logged In Success!")
                    return redirect('App_Shop:home')
    return render(request, 'App_Auth/login.html', context={'form': form})

@login_required
def logout_page(request):
    logout(request)
    messages.warning(request,"Loged Out Success!")
    return HttpResponseRedirect(reverse('App_Shop:home'))


@login_required
def change_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            form = ProfileForm(instance=profile)
            messages.success(request,"Profile Updated Successfully!")
            try:
                if request.GET['next']:
                    return redirect(request.GET['next'])
            except Exception as e:
                return redirect('App_Shop:home')
    return render(request, 'App_Auth/change_profile.html', context={'form': form})

