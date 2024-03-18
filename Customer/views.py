from django.shortcuts import render, redirect
from . models import *
import uuid
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


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

        # Assign the shipping order number
        shipment.booking_order_number = f'CARSO{shipment.id}'
        shipment.save()
        
        # Redirect to a success page
        messages.success(request, 'Success')
        return redirect('booking_details', shipment.uid)
    else:
        return render(request, 'shipment_booking_form.html')


def shipping_center_booking(request):
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
        shipment.save()
        
        # Redirect to a success page
        messages.success(request, 'Success')
        return redirect('booking_details', shipment.uid)
    else:
        return render(request, 'shipment_booking_form.html')


def booking_details(request,pk):
    try:
        uid=pk
        shipment = ShipmentBooking.objects.get(uid=uid)
        context={
            'data': shipment
        }
        return render(request, 'booking_details.html', context)
    except ShipmentBooking.DoesNotExist:
        return redirect('/')



def download_pdf(request,pk):
    # Get the template file path
    template_path = 'order_details_template.html'
    
    # Create a Django template object
    template = get_template(template_path)
    
    # Render the template with context data
    shipment = ShipmentBooking.objects.get(id=pk)
    context = {'data': shipment}  # Replace with your actual context data
    html = template.render(context)

    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Set the paper size to A4 (210mm x 297mm)
    pdf_options = {
        'page-size': 'A4',
        'margin-top': '20mm',  # Adjust margins as needed
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
    }

    # Generate PDF using xhtml2pdf with specified options
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=buffer, encoding='utf-8', show_error_as_pdf=True, **pdf_options)

    if not pdf.err:
        # Set the buffer's file pointer to the beginning for reading
        buffer.seek(0)
        
        # Create an HttpResponse with PDF content type and attachment header
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_details.pdf"'
        return response

    return HttpResponse('Error generating PDF: {}'.format(pdf.err), status=500)