from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login
from . models import *
from django.contrib import messages



#------------------ Login Section-------------------------

def login_page(request):
    return render(request,'login/login.html')

def login_save(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')


        
#------------------ Registration Section-------------------------

def register_page(request):
    return render(request,'register/registration.html')


def team_register(request):
    if request.method == 'POST':
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        designation=request.POST.get('designation')

        data=CargoTeam(
            first_name=first_name,last_name=last_name,
            email=email,username=username,password=password,designation=designation
        )
        data.save()
        messages.success(request,'Account Created, wait for approval...')
        return redirect('login_page')
    else:
        return redirect('register_page')

#------------------ Logout Section-------------------------

def admin_logout(request):
  auth.logout(request)
  return redirect('login_page')

# def logout(request):
#   request.session.pop('login_id', None)
#   return redirect('login_page')