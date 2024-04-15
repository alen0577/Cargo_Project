from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login




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


#------------------ Logout Section-------------------------

def admin_logout(request):
  auth.logout(request)
  return redirect('login_page')

# def logout(request):
#   request.session.pop('login_id', None)
#   return redirect('login_page')