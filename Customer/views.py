from django.shortcuts import render

# Create your views here.


# booking request page
def booking_request(request):
    return render(request, 'booking_request.html')

def home_pickup_booking(request):
    if request.method == 'POST':
        # If the form has been submitted
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        delivery_option = request.POST.get('delivery_option')
        delivery_type = request.POST.get('delivery_type')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        package_weight = request.POST.get('package_weight')
        number_of_packages = request.POST.get('number_of_packages')
        sender_name = request.POST.get('sender_name')
        sender_address = request.POST.get('sender_address')
        sender_city = request.POST.get('sender_city')
        sender_pincode = request.POST.get('sender_pincode')
        sender_state = request.POST.get('sender_state')
        sender_country = request.POST.get('sender_country')
        sender_contact_no = request.POST.get('sender_contact_no')
        receiver_name = request.POST.get('receiver_name')
        receiver_address = request.POST.get('receiver_address')
        receiver_city = request.POST.get('receiver_city')
        receiver_pincode = request.POST.get('receiver_pincode')
        receiver_state = request.POST.get('receiver_state')
        receiver_country = request.POST.get('receiver_country')
        receiver_contact_no = request.POST.get('receiver_contact_no')
        
        # Create an instance of the ShipmentBooking model
        shipment = ShipmentBooking(
            full_name=full_name,
            email=email,
            contact_number=contact_number,
            delivery_option=delivery_option,
            delivery_type=delivery_type,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            package_weight=package_weight,
            number_of_packages=number_of_packages,
            sender_name=sender_name,
            sender_address=sender_address,
            sender_city=sender_city,
            sender_pincode=sender_pincode,
            sender_state=sender_state,
            sender_country=sender_country,
            sender_contact_no=sender_contact_no,
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
        
        # Redirect to a success page
        return redirect('success_url')
    else:
        return render(request, 'shipment_booking_form.html')