from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,ShipmentTracking,CustomerIssues,OrderQueries
from Admin.models import ServiceLocation,City,Notifications
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


# executive shipment update page
def shipment_status_update(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_arrived=False,is_delivered=False,is_returned=False)
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'shipment/shipment_status.html', context)
    else:
        return redirect('/')


def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        today=date.today()
        order = ShipmentTracking.objects.get(id=order_id)
        order.status = status
        if status == 'dispatched':
            order.shipped_date=today
        if status == 'arrived_at_destination_hub':
            order.is_arrived=True
            order.destination_hub_arrival_date=today
            
            # notification section
            title = 'Order Delivery'
            message = 'Your center receives an order for delivery updates that requires immediate attention to ensure timely processing and accurate tracking.'
            pincode = order.shipment.receiver_pincode
            postal_code=ServiceLocation.objects.get(postal_code=pincode)
            notification = Notifications(title=title,message=message,recipient_center=postal_code.city)
            notification.save()

        order.save()

        orders = ShipmentTracking.objects.filter(is_arrived=False,is_delivered=False,is_returned=False)
        orders_data = [{
            'id': order.id,
            'date': order.shipment.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})
        

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def all_shipment_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(arrived_for_return=False).order_by('-shipment__date')
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'shipment/all_orders_status.html', context)
    else:
        return redirect('/')

def all_shipment_orders_by_date(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(shipment__date__range=[from_date, to_date],arrived_for_return=False).order_by('-shipment__date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(shipment__date__gte=from_date,arrived_for_return=False).order_by('-shipment__date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(shipment__date__lte=to_date,arrived_for_return=False).order_by('-shipment__date')
        else:
            orders = ShipmentTracking.objects.filter(arrived_for_return=False).order_by('-shipment__date')
        
        orders_data = [{
            'id': order.id,
            'date': order.shipment.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})



# executive return shipment update page

def executive_return_management(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        
        context = {
            'details': dash_details,
            
        }
        return render(request, 'return-section/return_management.html', context)
    else:
        return redirect('/')


def return_shipment_status(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=False)
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'return-section/return_shipment_status.html', context)
    else:
        return redirect('/')


def update_return_order_status(request,pk):

    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        if request.method == 'POST':
            order_id = pk
            status = request.POST['status']
            location = request.POST['current_location']
            expected_date = request.POST['estimated_delivery_date']
            today=date.today()
            order = ShipmentTracking.objects.get(id=order_id)
            order.return_status = status
            order.current_return_location=location
            if expected_date:
                order.estimated_delivery_date=expected_date
            if status == 'dispatched':
                order.return_shipped_date=today
            if status == 'arrived_at_destination_hub':
                order.arrived_for_return=True
                order.destination_hub_return_arrival_date=today
                
                # notification section
                title = 'Return Delivery'
                order_number=order.shipment.booking_order_number
                message = f'Your center has received an order with the number {order_number} for return delivery updates. Immediate attention is required to ensure timely processing and accurate tracking.'
                return_center=order.shipment.shipping_center
                notification = Notifications(title=title,message=message,recipient_center=return_center)
                notification.save()

            order.save()
            # Redirect to a success page
            messages.success(request, 'Updated')
            return redirect('return_shipment_status')

        
        
    else:
        return redirect('/')

    
        
        

    

def all_return_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_returned=True).order_by('-return_processed_date')
        
        context = {
            'details': dash_details,
            'orders': orders,
        }
        return render(request, 'return-section/all_return_orders.html', context)
    else:
        return redirect('/')

def return_status_by_date(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__range=[from_date, to_date],is_returned=True).order_by('-return_processed_date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__gte=from_date,is_returned=True).order_by('-return_processed_date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__lte=to_date,is_returned=True).order_by('-return_processed_date')
        else:
            orders = ShipmentTracking.objects.filter(is_returned=True).order_by('-return_processed_date')
        
        orders_data = [{
            'id': order.id,
            'date': order.return_processed_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.return_status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})





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


def query_action_taken(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        query=OrderQueries.objects.get(id=pk,action_taken=0)
        if request.method == 'POST':
            query.action_taken=1
            query.response=request.POST.get('response')
            query.save()
            messages.success(request,'Action Taken')
            return redirect('pending_queries')  
        else:
            return redirect('pending_queries',)

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
