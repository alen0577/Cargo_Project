from django.shortcuts import render, redirect, get_object_or_404
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,ShipmentTracking,CustomerIssues
from Admin.models import ServiceLocation, City, Notifications
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta
from django.http import JsonResponse
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# Create your views here.

# -------------------------------team section--------------------------------

# team dashboard
def team_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order_count=ShipmentBooking.objects.filter(is_confirmed=0,is_active=1).count()
        pickup_count=ShipmentBooking.objects.filter(is_confirmed=1,is_active=1).count()
        bill_count=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1).count()
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

       
        context = {
            'details': dash_details,
            'order_count':order_count,
            'pickup_count':pickup_count,
            'bill_count':bill_count,
            'noti_count':noti_count,
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
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'city': city,
            'noti_count':noti_count,
        }
        return render(request, 'team_profile.html', context)
    else:
        return redirect('/')


# team profile edit page
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
            center_id=request.POST.get('center-select')
            print(center_id)
            center=City.objects.get(id=center_id)
            data.work_center=center
            if img:
                data.profile_picture=img
        
            data.save()
            messages.success(request,'Updated')
            return redirect('team_profile')
        else:
            return redirect('team_profile')
    else:
        return redirect('/')


# order booking  page
def order_booking(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        city = City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       
        context = {
            'details': dash_details,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'order_booking.html', context)
    else:
        return redirect('/')

def order_booking_save(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        if request.method == 'POST':
            # If the form has been submitted
            
            shipment_type = 'Shipping Center'
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            delivery_option = request.POST.get('delivery_option')
            delivery_type = request.POST.get('delivery_type')
            package_weight = request.POST.get('package_weight')
            number_of_packages = request.POST.get('number_of_packages')
            receiver_name = request.POST.get('receiver_name')
            receiver_address = request.POST.get('receiver_address')
            receiver_city = request.POST.get('receiver_city')
            receiver_pincode = request.POST.get('receiver_pincode')
            receiver_state = request.POST.get('receiver_state')
            receiver_country = request.POST.get('receiver_country')
            receiver_contact_no = request.POST.get('receiver_contact_no')
            shipping_center_id = request.POST.get('center-select')
            center=City.objects.get(id=shipping_center_id)
            
            # Create an instance of the ShipmentBooking model
            shipment = ShipmentBooking(
                shipment_type=shipment_type,
                full_name=full_name,
                email=email,
                contact_number=contact_number,
                delivery_option=delivery_option,
                delivery_type=delivery_type,
                package_weight=package_weight,
                number_of_packages=number_of_packages,
                shipping_center=center,
                receiver_name=receiver_name,
                receiver_address=receiver_address,
                receiver_city=receiver_city,
                receiver_pincode=receiver_pincode,
                receiver_state=receiver_state,
                receiver_country=receiver_country,
                receiver_contact_no=receiver_contact_no
            )
            
            # Save the instance to the database
            shipment.save()

            # Assign the shipping order number
            shipment.booking_order_number = f'CARSO{shipment.id}'
            shipment.is_confirmed=2
            shipment.save()
 
            # Redirect to a success page
            return redirect('bill_request_details', shipment.id)
        else:
            return redirect('order_booking') 
    else:
        return redirect('/')


def check_pincode(request):
    pincode = request.GET.get('pincode')
    is_available = ServiceLocation.objects.filter(postal_code=pincode).exists()
    return JsonResponse({'is_available': is_available})



# order request page
def order_requests(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=0,is_active=1).order_by('date','time')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
 
        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'orders/order_requests.html', context)
    else:
        return redirect('/')

def fetch_orders_by_city(request):
    city = request.GET.get('city')
    orders = ShipmentBooking.objects.filter(sender_city=city,shipment_type='Home Pickup',is_confirmed=0,is_active=1).order_by('date','time')
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
        }
        for order in orders
    ]
   
    return JsonResponse({'orders': orders_data})

def fetch_orders_by_type(request):
    order_type = request.GET.get('type')
    orders = ShipmentBooking.objects.filter(shipment_type=order_type,is_confirmed=0,is_active=1).order_by('date','time')  # Adjust the field name based on your model
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
        }
        for order in orders
    ]
    return JsonResponse({'orders': orders_data})



def order_request_details(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=0,is_active=1)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        
        context = {
            'details': dash_details,
            'order': order,
            'noti_count':noti_count,
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


# def order_approval(request, pk):
#     if 'login_id' in request.session:
#         log_id = request.session['login_id']
#         dash_details = get_object_or_404(CargoTeam, id=log_id, admin_approval=1, is_active=1)
#         order = get_object_or_404(ShipmentBooking, id=pk, is_confirmed=0, is_active=1)
        
#         if request.method == 'POST':
            
#             order.pickup_date = request.POST.get('pickupdate')
#             order.description = request.POST.get('description')
            
#             if order.shipment_type == 'Home Pickup':
#                 order.is_confirmed = 1
#             else:
#                 order.is_confirmed = 2
            
#             order.save()
#             return JsonResponse({'success': True, 'message': 'Order Confirmed'})
            
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid request method'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Unauthorized access'})

def order_rejection(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=0,is_active=1)
        if request.method == 'POST':
            order.description=request.POST.get('description')
            order.is_confirmed=4
            order.save()
            messages.success(request,'Order Rejected')
            return redirect('order_requests')  
        else:
            return redirect('order_requests')

    else:
        return redirect('/')

def fetch_orders(request):
    if 'login_id' in request.session:
        orders = ShipmentBooking.objects.filter(is_confirmed=0, is_active=1)
        order_list = []
        for order in orders:
            order_list.append({
                'id': order.id,
                'date': order.date,
                'booking_order_number': order.booking_order_number,
                'full_name': order.full_name,
                'email': order.email,
                'contact_number': order.contact_number,
                'sender_city': order.sender_city,
                'pickup_date': order.pickup_date,
                'description': order.description,
            })
        return JsonResponse({'orders': order_list})
    else:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)


def pickup_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=1,is_active=1).order_by('date','time')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'orders/pickup_orders.html', context)
    else:
        return redirect('/')

def pickup_orders_by_city(request):
    city = request.GET.get('city')
    filter_date = request.GET.get('filter_date')
    
    today = date.today()
    
    if city:
        if filter_date == "Today":
            orders = ShipmentBooking.objects.filter(sender_city=city, pickup_date=today,is_confirmed=1,is_active=1).order_by('date','time')
        else:
            orders = ShipmentBooking.objects.filter(sender_city=city,is_confirmed=1,is_active=1).order_by('date','time')

    else:
        if filter_date == "Today":
            orders = ShipmentBooking.objects.filter(pickup_date=today,is_confirmed=1,is_active=1).order_by('date','time')
        else:
            orders = ShipmentBooking.objects.filter(is_confirmed=1,is_active=1).order_by('date','time')
    
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
            'sender_city': order.sender_city,
            'pickup_date': order.pickup_date.strftime('%d-%m-%Y'),
            'description': order.description,
        })

    return JsonResponse({'orders': orders_data})


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


def bill_request_approve(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=1,is_active=1)
        if request.method == 'POST':
            order.is_confirmed=2
            order.save()
            return redirect('bill_request_details', order.id)  
        else:
            return redirect('pickup_order_details', order.id)

    else:
        return redirect('/')

def bill_requests(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1).order_by('date','time')
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       
        context = {
            'details': dash_details,
            'orders': orders,
            'noti_count':noti_count,
        }
        return render(request, 'orders/bill_requests.html', context)
    else:
        return redirect('/')


def bill_request_details(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=2,is_active=1)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       
        context = {
            'details': dash_details,
            'data': order,
            'noti_count':noti_count,
        }
        return render(request, 'orders/bill_request_details.html', context)
    else:
        return redirect('/')


def bill_save(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order=ShipmentBooking.objects.get(id=pk,is_confirmed=2,is_active=1)
        if request.method == 'POST':
            # create ShipmentTracking record
            tracking= ShipmentTracking(shipment=order)
            tracking.save()
            
            order.is_confirmed=3
            order.save()

            
            
            messages.success(request, 'Payment Done and Order moved for delivery process')
            return redirect('bill_requests')  
        else:
            return redirect('bill_requests',)

    else:
        return redirect('/')


def all_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'orders/all_orders.html', context)
    else:
        return redirect('/')

def fetch_allorders_by_type(request):
    order_type = request.GET.get('type')
    orders = ShipmentBooking.objects.filter(shipment_type=order_type,is_active=1).exclude(is_confirmed=4).order_by('-date','-time')  # Adjust the field name based on your model
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
            'status':order.is_confirmed,
        }
        for order in orders
    ]
    return JsonResponse({'orders': orders_data})

def fetch_allorders_by_city(request):
    city = request.GET.get('city')
    orders = ShipmentBooking.objects.filter(sender_city=city,shipment_type='Home Pickup',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
            'status':order.is_confirmed,
        }
        for order in orders
    ]
   
    return JsonResponse({'orders': orders_data})

def fetch_allpickuporders_by_date(request):
    city = request.GET.get('city')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        orders = ShipmentBooking.objects.filter(date__range=[from_date, to_date],sender_city=city,shipment_type='Home Pickup',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    elif from_date:
        orders = ShipmentBooking.objects.filter(date__gte=from_date,sender_city=city,shipment_type='Home Pickup',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    elif to_date:
        orders = ShipmentBooking.objects.filter(date__lte=to_date,sender_city=city,shipment_type='Home Pickup',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    else:
        orders = ShipmentBooking.objects.filter(sender_city=city,shipment_type='Home Pickup',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')

    orders_data = [{
        'id': order.id,
        'date': order.date.strftime('%d-%m-%Y'),
        'booking_order_number': order.booking_order_number,
        'full_name': order.full_name,
        'email': order.email,
        'contact_number': order.contact_number,
        'status':order.is_confirmed,
    } for order in orders]

    return JsonResponse({'orders': orders_data})


def fetch_allshipcenterorders_by_date(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        orders = ShipmentBooking.objects.filter(date__range=[from_date, to_date],shipment_type='Shipping Center',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    elif from_date:
        orders = ShipmentBooking.objects.filter(date__gte=from_date,shipment_type='Shipping Center',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    elif to_date:
        orders = ShipmentBooking.objects.filter(date__lte=to_date,shipment_type='Shipping Center',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')
    else:
        orders = ShipmentBooking.objects.filter(shipment_type='Shipping Center',is_active=1).exclude(is_confirmed=4).order_by('-date','-time')

    orders_data = [{
        'id': order.id,
        'date': order.date.strftime('%d-%m-%Y'),
        'booking_order_number': order.booking_order_number,
        'full_name': order.full_name,
        'email': order.email,
        'contact_number': order.contact_number,
        'status':order.is_confirmed,
    } for order in orders]

    return JsonResponse({'orders': orders_data})



def rejected_orders(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders=ShipmentBooking.objects.filter(is_confirmed=4,is_active=1).order_by('-date','-time')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'orders/rejected_orders.html', context)
    else:
        return redirect('/')


def fetch_rejectedorders_by_type(request):
    order_type = request.GET.get('type')
    orders = ShipmentBooking.objects.filter(shipment_type=order_type,is_confirmed=4,is_active=1).order_by('-date','-time')  # Adjust the field name based on your model
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
            'reason':order.description,
        }
        for order in orders
    ]
    return JsonResponse({'orders': orders_data})

def fetch_rejectedorders_by_city(request):
    city = request.GET.get('city')
    orders = ShipmentBooking.objects.filter(sender_city=city,shipment_type='Home Pickup',is_confirmed=4,is_active=1).order_by('-date','-time')
    orders_data = [
        {
            'id': order.id,
            'date': order.date.strftime('%d-%m-%Y'),
            'booking_order_number': order.booking_order_number,
            'full_name': order.full_name,
            'email': order.email,
            'contact_number': order.contact_number,
            'reason':order.description,
        }
        for order in orders
    ]
   
    return JsonResponse({'orders': orders_data})

def fetch_rejectedpickuporders_by_date(request):
    city = request.GET.get('city')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        orders = ShipmentBooking.objects.filter(date__range=[from_date, to_date],sender_city=city,shipment_type='Home Pickup',is_active=1,is_confirmed=4).order_by('-date','-time')
    elif from_date:
        orders = ShipmentBooking.objects.filter(date__gte=from_date,sender_city=city,shipment_type='Home Pickup',is_active=1,is_confirmed=4).order_by('-date','-time')
    elif to_date:
        orders = ShipmentBooking.objects.filter(date__lte=to_date,sender_city=city,shipment_type='Home Pickup',is_active=1,is_confirmed=4).order_by('-date','-time')
    else:
        orders = ShipmentBooking.objects.filter(sender_city=city,shipment_type='Home Pickup',is_active=1,is_confirmed=4).order_by('-date','-time')

    orders_data = [{
        'id': order.id,
        'date': order.date.strftime('%d-%m-%Y'),
        'booking_order_number': order.booking_order_number,
        'full_name': order.full_name,
        'email': order.email,
        'contact_number': order.contact_number,
        'reason':order.description,
    } for order in orders]

    return JsonResponse({'orders': orders_data})


def fetch_rejectedshipcenterorders_by_date(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        orders = ShipmentBooking.objects.filter(date__range=[from_date, to_date],shipment_type='Shipping Center',is_active=1,is_confirmed=4).order_by('-date','-time')
    elif from_date:
        orders = ShipmentBooking.objects.filter(date__gte=from_date,shipment_type='Shipping Center',is_active=1,is_confirmed=4).order_by('-date','-time')
    elif to_date:
        orders = ShipmentBooking.objects.filter(date__lte=to_date,shipment_type='Shipping Center',is_active=1,is_confirmed=4).order_by('-date','-time')
    else:
        orders = ShipmentBooking.objects.filter(shipment_type='Shipping Center',is_active=1,is_confirmed=4).order_by('-date','-time')

    orders_data = [{
        'id': order.id,
        'date': order.date.strftime('%d-%m-%Y'),
        'booking_order_number': order.booking_order_number,
        'full_name': order.full_name,
        'email': order.email,
        'contact_number': order.contact_number,
        'reason':order.description,
    } for order in orders]

    return JsonResponse({'orders': orders_data})


# customer support section
def customer_support(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        issues_count = CustomerIssues.objects.filter(action_taken=0).count()
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
        
        context = {
            'details': dash_details,
            'issues_count':issues_count,
            'noti_count':noti_count,
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
        pending_issues = CustomerIssues.objects.filter(action_taken=0).order_by('date','time')
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       
        context = {
            'details': dash_details,
            'issues':pending_issues,
            'noti_count':noti_count,
        }
        return render(request, 'customersupport/pending_issues.html', context)
    else:
        return redirect('/')


def issue_action_taken(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        issue=CustomerIssues.objects.get(id=pk,action_taken=0)
        if request.method == 'POST':
            issue.action_taken=1
            issue.response=request.POST.get('response')
            issue.save()
            messages.success(request,'Action Taken')
            return redirect('pending_issues')  
        else:
            return redirect('pending_issues',)

    else:
        return redirect('/')


def solved_issues(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        solved_issues = CustomerIssues.objects.filter(action_taken=1).order_by('-date','-time')
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
        
        context = {
            'details': dash_details,
            'issues':solved_issues,
            'noti_count':noti_count,
        }
        return render(request, 'customersupport/solved_issues.html', context)
    else:
        return redirect('/')


# delivery management section
def delivery_management(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        pending_count=ShipmentTracking.objects.filter(is_arrived=True,is_returned=False,is_delivered=False).count()
        all_count=ShipmentTracking.objects.filter(is_arrived=True,).count()
        bill_count=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1).count()
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       

        
        context = {
            'details': dash_details,
            'pending_count':pending_count,
            'all_count':all_count,
            'bill_count':bill_count,
            'noti_count':noti_count,
        }
        return render(request, 'delivery/delivery_management.html', context)
    else:
        return redirect('/')


def pending_deliveries(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_arrived=True,is_returned=False,is_delivered=False).order_by('destination_hub_arrival_date')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
            
        }
        return render(request, 'delivery/pending_deliveries.html', context)
    else:
        return redirect('/')

def pending_deliveries_by_city(request):
    if request.method == 'POST':
       
        city = request.POST.get('city')
        orders = ShipmentTracking.objects.filter(shipment__receiver_city=city,is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')
        orders_data = [{
            'id': order.id,
            'date': order.destination_hub_arrival_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})

def pending_deliveries_by_date(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__range=[from_date, to_date],shipment__receiver_city=city,is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__gte=from_date,shipment__receiver_city=city,is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__lte=to_date,shipment__receiver_city=city,is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')
        elif city:
            orders = ShipmentTracking.objects.filter(shipment__receiver_city=city,is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')
        else:
            orders = ShipmentTracking.objects.filter(is_arrived=True,is_returned=False,is_delivered=False).order_by('-destination_hub_arrival_date')

        
        orders_data = [{
            'id': order.id,
            'date': order.destination_hub_arrival_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})

def update_pending_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        order = ShipmentTracking.objects.get(id=order_id)
        order.status = status
        order.save()

        
        return JsonResponse({'success': True,})



def all_deliveries(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_arrived=True).order_by('destination_hub_arrival_date')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'delivery/all_deliveries.html', context)
    else:
        return redirect('/')


def all_deliveries_by_city(request):
    if request.method == 'POST':
       
        city = request.POST.get('city')
        orders = ShipmentTracking.objects.filter(shipment__receiver_city=city,is_arrived=True).order_by('-destination_hub_arrival_date')
        orders_data = [{
            'id': order.id,
            'date': order.destination_hub_arrival_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})


def all_deliveries_by_date(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__range=[from_date, to_date],shipment__receiver_city=city,is_arrived=True).order_by('-destination_hub_arrival_date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__gte=from_date,shipment__receiver_city=city,is_arrived=True).order_by('-destination_hub_arrival_date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(destination_hub_arrival_date__lte=to_date,shipment__receiver_city=city,is_arrived=True).order_by('-destination_hub_arrival_date')
        else:
            orders = ShipmentTracking.objects.filter(shipment__receiver_city=city,is_arrived=True).order_by('-destination_hub_arrival_date')
        
        orders_data = [{
            'id': order.id,
            'date': order.destination_hub_arrival_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})

# end


# return management section
def return_management(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        pending_count=ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True,returned=False).count()
        all_count=ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True).count()
        bill_count=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1).count()
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
       

        
        context = {
            'details': dash_details,
            'pending_count':pending_count,
            'all_count':all_count,
            'bill_count':bill_count,
            'noti_count':noti_count,
        }
        return render(request, 'return/return_management.html', context)
    else:
        return redirect('/')


def pending_returns(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
   
        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
            
        }
        return render(request, 'return/pending_returns.html', context)
    else:
        return redirect('/')

def pending_returns_by_city(request):
    if request.method == 'POST':
       
        city = request.POST.get('city')
        orders = ShipmentTracking.objects.filter(shipment__sender_city=city,is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        orders_data = [{
            'id': order.id,
            'date': order.return_processed_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.return_status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})

def pending_returns_by_date(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__range=[from_date, to_date],shipment__sender_city=city,is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__gte=from_date,shipment__sender_city=city,is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__lte=to_date,shipment__sender_city=city,is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        elif city:
            orders = ShipmentTracking.objects.filter(shipment__sender_city=city,is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')
        else:
            orders = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True,returned=False).order_by('return_processed_date')

        
        orders_data = [{
            'id': order.id,
            'date': order.return_processed_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.return_status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})

def update_pending_return_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        order = ShipmentTracking.objects.get(id=order_id)
        order.return_status = status
        order.save()

        
        return JsonResponse({'success': True,})



def all_returns(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        city=City.objects.filter(is_active=True)
        today=date.today()
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()

        context = {
            'details': dash_details,
            'orders': orders,
            'city':city,
            'noti_count':noti_count,
        }
        return render(request, 'return/all_returns.html', context)
    else:
        return redirect('/')


def all_returns_by_city(request):
    if request.method == 'POST':
       
        city = request.POST.get('city')
        orders = ShipmentTracking.objects.filter(shipment__sender_city=city,is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        orders_data = [{
            'id': order.id,
            'date': order.return_processed_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.return_status,
        } for order in orders]
        return JsonResponse({'success': True,'orders': orders_data})


def all_returns_by_date(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__range=[from_date, to_date],shipment__sender_city=city,is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        elif from_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__gte=from_date,shipment__sender_city=city,is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        elif to_date:
            orders = ShipmentTracking.objects.filter(return_processed_date__lte=to_date,shipment__sender_city=city,is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        elif city:
            orders = ShipmentTracking.objects.filter(shipment__sender_city=city,is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        else:
            orders = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=True).order_by('-return_processed_date')
        
        orders_data = [{
            'id': order.id,
            'date': order.return_processed_date.strftime('%d-%m-%Y'),
            'booking_order_number': order.shipment.booking_order_number,
            'status': order.return_status,
        } for order in orders]
        
        return JsonResponse({'success': True,'orders': orders_data})

# team notifications
def team_notifications(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        order_count=ShipmentBooking.objects.filter(is_confirmed=0,is_active=1).count()
        pickup_count=ShipmentBooking.objects.filter(is_confirmed=1,is_active=1).count()
        bill_count=ShipmentBooking.objects.filter(is_confirmed=2,is_active=1).count()
        today=date.today()
        notifications = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).order_by('-date_created','-time_created')
        noti_count = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).count()
        noti_status = Notifications.objects.filter(recipient_center=dash_details.work_center,date_created=today).update(is_read=True)

        
        context = {
            'details': dash_details,
            'order_count':order_count,
            'pickup_count':pickup_count,
            'bill_count':bill_count,
            'notifications':notifications,
            'noti_count':noti_count,
        }
        return render(request, 'team_notifications.html', context)
    else:
        return redirect('/')




