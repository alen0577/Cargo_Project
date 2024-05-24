from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,CustomerIssues
from Admin.models import ServiceLocation
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta


# Create your views here.

# -------------------------------executive section--------------------------------

# executive dashboard
def executive_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
            
        }
        return render(request, 'executive_dashboard.html', context)
    else:
        return redirect('/')


# executive profile page
def executive_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
        }
        return render(request, 'executive_profile.html', context)
    else:
        return redirect('/')
