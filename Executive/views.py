from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,ShipmentTracking,CustomerIssues,OrderQueries
from Admin.models import ServiceLocation
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta
from django.http import JsonResponse


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


# executive profile editpage
def edit_executive_profile(request):
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
            return redirect('executive_profile')
        else:
            return redirect('executive_profile')
    else:
        return redirect('/')


# executive profile page
def shipment_status_update(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.all()
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'shipment_status.html', context)
    else:
        return redirect('/')


def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        order = ShipmentTracking.objects.get(id=order_id)
        order.status = status
        order.save()

        orders = ShipmentTracking.objects.all()
        orders_data = [{
            'id': order.id,
            'date': order.shipment.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})
        

    return JsonResponse({'success': False, 'error': 'Invalid request'})



# Order queries section page
def query_section(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        query_count = OrderQueries.objects.filter(action_taken=0).count()

        context = {
            'details': dash_details,
            'query_count':query_count
        }
        
        return render(request, 'order_queries/query_section.html', context)
    else:
        return redirect('/')

def pending_queries(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        pending_queries = OrderQueries.objects.filter(action_taken=0).order_by('date','time')
        
        context = {
            'details': dash_details,
            'queries':pending_queries,
        }
        return render(request, 'order_queries/pending_queries.html', context)
    else:
        return redirect('/')



def all_queries(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        all_queries = OrderQueries.objects.all().order_by('-date','-time')
        
        context = {
            'details': dash_details,
            'queries':all_queries,
        }
        return render(request, 'order_queries/all_queries.html', context)
    else:
        return redirect('/')
