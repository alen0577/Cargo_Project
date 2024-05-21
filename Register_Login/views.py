from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse



#------------------ Login Section-------------------------

def login_page(request):
    return render(request,'login/login.html')

def login_save(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)

        # admin login session
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        
        try:
            log_user = CargoTeam.objects.get(username=username, password=password)
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Username or Password. Try Again.')
            return redirect('login_page')

        # team member login session
        if log_user.designation == 'Team Member':
            request.session["login_id"] = log_user.id
            if 'login_id' in request.session:
                member_id = request.session['login_id']
            else:
                return redirect('login_page')

            try:
                dash_details = CargoTeam.objects.get(id=member_id,admin_approval=1,is_active=1)
                return redirect('team_dashboard')
            except CargoTeam.DoesNotExist:
                messages.warning(request, 'Approval is Pending')
                return redirect('login_page')

        # executive member login session
        elif log_user.designation == 'Executive Member':
            request.session["login_id"] = log_user.id
            if 'login_id' in request.session:
                member_id = request.session['login_id']
            else:
                return redirect('login_page')

            try:
                dash_details = CargoTeam.objects.get(id=member_id,admin_approval=1,is_active=1)
                return redirect('executive_dashboard')
            except CargoTeam.DoesNotExist:
                messages.warning(request, 'Approval is Pending')
                return redirect('login_page')

        else:
            return render(request, 'error-404.html')
    else:
        return redirect('login_page')
    
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

# username checking
def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if CargoTeam.objects.filter(username=username).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})



#------------------ Logout Section-------------------------

def admin_logout(request):
  auth.logout(request)
  return redirect('login_page')

def logout(request):
  request.session.pop('login_id', None)
  return redirect('login_page')