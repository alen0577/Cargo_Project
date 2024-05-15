from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,CustomerIssues
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



def order_booking(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
        }
        return render(request, 'order_booking.html', context)
    else:
        return redirect('/')




# order request page
def order_requests(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=0,is_active=1).order_by('-date','-time')
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'orders/order_requests.html', context)
    else:
        return redirect('/')



def order_request_details(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=0,is_active=1)
        
        context = {
            'details': dash_details,
            'order': order,
        }
        return render(request, 'orders/order_request_details.html', context)
    else:
        return redirect('/')


def order_approval(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=0,is_active=1)
        if request.method == 'POST':
            order.pickup_date=request.POST.get('pickupdate')
            order.description=request.POST.get('description')
            if order.shipment_type == 'Home Pickup':
                order.is_confirmed=1
            else:
                order.is_confirmed=2

            order.save()
            messages.success(request,'Order Confirmed')
            return redirect('order_requests')  
        else:
            return redirect('order_requests')

    else:
        return redirect('/')

def order_rejection(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=0,is_active=1)
        if request.method == 'POST':
            order.description=request.POST.get('description')
            order.is_confirmed=3
            order.save()
            messages.success(request,'Order Rejected')
            return redirect('order_requests')  
        else:
            return redirect('order_requests')

    else:
        return redirect('/')

def pickup_orders(request):
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
        return render(request, 'orders/pickup_orders.html', context)
    else:
        return redirect('/')


def pickup_order_details(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=1,is_active=1)
        
        context = {
            'details': dash_details,
            'order': order,
        }
        return render(request, 'orders/pickup_order_details.html', context)
    else:
        return redirect('/')


def edit_pickup_order_details(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=1,is_active=1)
        
        if request.method == 'POST':
            order.package_weight=request.POST.get('package_weight')
            order.number_of_packages=request.POST.get('number_of_packages')
            order.save()
            messages.success(request,'Details Updated')
            return redirect('pickup_order_details', order.id) 
        else:
            return redirect('pickup_order_details', order.id)

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



# customer support section
def customer_support(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
        }
        return render(request, 'customersupport/customer_support.html', context)
    else:
        return redirect('/')


def pending_issues(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        pending_issues = CustomerIssues.objects.filter(action_taken=0)
        
        context = {
            'details': dash_details,
            'issues':pending_issues,
        }
        return render(request, 'customersupport/pending_issues.html', context)
    else:
        return redirect('/')

def solved_issues(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        solved_issues = CustomerIssues.objects.filter(action_taken=1)
        
        context = {
            'details': dash_details,
            'issues':solved_issues,
        }
        return render(request, 'customersupport/solved_issues.html', context)
    else:
        return redirect('/')