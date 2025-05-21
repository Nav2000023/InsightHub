from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib import auth

# Create your views here.

def register_page(request):
    return render(request, 'accounts/register.html')

def login_page(request):
    return render(request,'accounts/login.html')

def logout(request):
    try:
        auth.logout(request)
    except:
        pass
    messages.success(request, 'Logged out successfully')
    return redirect("index")
