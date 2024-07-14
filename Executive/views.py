from django.shortcuts import render, redirect
from Register_Login.models import CargoTeam
from Customer.models import ShipmentBooking,ShipmentTracking,CustomerIssues,OrderQueries
from Admin.models import ServiceLocation,City,Notifications
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

# -------------------------------executive section--------------------------------

# executive dashboard
def executive_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        orders_count = ShipmentTracking.objects.filter(is_arrived=False,is_delivered=False,is_returned=False).count()

        context = {
            'details': dash_details,
            'orders_count':orders_count,
            
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


def update_order_status(request,pk):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        dash_details = CargoTeam.objects.get(id=log_id,admin_approval=1,is_active=1)
        if request.method == 'POST':
            order_id = pk
            status = request.POST.get('status')
            location = request.POST['current_location']
            expected_date = request.POST['estimated_delivery_date']
            today=date.today()
            order = ShipmentTracking.objects.get(id=order_id)
            order.status = status
            order.current_location=location
            if expected_date:
                order.estimated_delivery_date=expected_date
            if status == 'dispatched':
                order.shipped_date=today
            if status == 'arrived_at_destination_hub':
                order.is_arrived=True
                order.destination_hub_arrival_date=today
                
                # notification section
                title = 'Order Delivery'
                order_number=order.shipment.booking_order_number
                message = f'Your center has received an order with the number {order_number} for delivery updates. Immediate attention is required to ensure timely processing and accurate tracking.'
                pincode = order.shipment.receiver_pincode
                postal_code=ServiceLocation.objects.get(postal_code=pincode)
                notification = Notifications(title=title,message=message,recipient_center=postal_code.city)
                notification.save()

            order.save()
            # Redirect to a success page
            messages.success(request, 'Updated')
            return redirect('shipment_status_update')   
        else:
            return redirect('/')
    else:
        return redirect('/')

        
        

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
            'tracking_number': order.tracking_number,
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
        orders_count = ShipmentTracking.objects.filter(is_returned=True,arrived_for_return=False).count()
        
        context = {
            'details': dash_details,
            'orders_count':orders_count,
            
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
            'tracking_number': order.tracking_number,
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

            # mail sending section
            customer_name=query.name
            queries=query.queries
            response=query.response
            tracking_number=query.tracking_number
            order=ShipmentTracking.objects.get(tracking_number=tracking_number)
            email=order.shipment.email

            subject = f'Response to Your Order Query {tracking_number}'
            message = f'''
            Dear {customer_name},

            Thank you for reaching out to us with your query regarding order {tracking_number}.
            We have reviewed your inquiry and would like to provide you with the following information:

            Here are the details:

            - Tracking Number: {tracking_number}
            - Query: {queries}
            - Response/Action: {response}
            
            We hope this information helps address your query. 
            If you have any other questions or need further assistance, please feel free to contact us.

            Best regards,
            Cargo
            info@altostechnologies.com
            +91 90741 56818
            '''

            recipient_email = email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

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

            # mail sending section
            customer_name=issue.full_name
            issues=issue.issues
            response=issue.response
            delivery_date=date.today()
           

            subject = f'Regarding Your Recent Issue/Help Request'
            message = f'''
            Dear {customer_name},

            Thank you for reaching out to us regarding your recent issue/help request. 
            We have reviewed your issues/help and would like to provide you with the following information:

            Here are the details:

            - Issue: {issues}
            - Response/Action: {response}

            In the meantime, if you have any additional information or questions, 
            please feel free to reply to this email or contact our support team at support@example.com or (123) 456-7890.

            We appreciate your patience and understanding.
            
            Best regards,
            Cargo
            info@altostechnologies.com
            +91 90741 56818
            '''

            recipient_email = issue.email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])


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

