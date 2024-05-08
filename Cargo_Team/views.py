from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta

# Create your views here.

# -------------------------------team section--------------------------------

# team dashboard
def team_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
        }
        return render(request, 'team_dashboard.html', context)
    else:
        return redirect('/')

# team profile page
def team_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
        }
        return render(request, 'team_profile.html', context)
    else:
        return redirect('/')


# team profile page
def edit_team_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        data = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        if request.method == 'POST':
            img=request.FILES.get('image')
            data.first_name=request.POST.get('fname')
            data.last_name=request.POST.get('lname')
            data.username=request.POST.get('uname')
            data.email=request.POST.get('email')
            data.address=request.POST.get('address')
            data.city=request.POST.get('city')
            data.state=request.POST.get('state')
            data.country=request.POST.get('country')
            data.contact=request.POST.get('contact')
            data.pincode=request.POST.get('pincode')
            if img:
                data.profile_picture=img
        
            data.save()
            messages.success(request,'Updated')
            return redirect('team_profile')
        else:
            return redirect('team_profile')
    else:
        return redirect('/')

# team profile page
def order_requests(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=0,is_active=1)
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'orders/order_requests.html', context)
    else:
        return redirect('/')

def approved_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=1,is_active=1)
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'orders/approved_orders.html', context)
    else:
        return redirect('/')

def rejected_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1)
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'orders/rejected_orders.html', context)
    else:
        return redirect('/')