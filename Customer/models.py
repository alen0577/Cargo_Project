from django.db import models
import uuid
import qrcode  # Add this line to import the qrcode library
from io import BytesIO
from django.core.files import File

# Create your models here.

# Shipment booking model

class ShipmentBooking(models.Model):

    # unique id 
    uid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    booking_order_number = models.CharField(max_length=20,unique=True,null=True,blank=True)

    # Shipment type field
    shipment_type = models.CharField(max_length=30,default='Home Pickup')

    # customer details
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length = 254,null=True,blank=True)
    contact_number = models.CharField(max_length=100,null=True,blank=True)

    # shipment details
    delivery_option_choices = [
        ('road', 'By Road'),
        ('air', 'By Air'),
        ('sea', 'By Sea')
    ]
    delivery_option = models.CharField(max_length=10,choices=delivery_option_choices,null=True,blank=True)
    delivery_type_choices = [
        ('normal', 'Normal'),
        ('speed', 'Speed')
    ]
    delivery_type = models.CharField(max_length=10,choices=delivery_type_choices,null=True,blank=True)
    pickup_date = models.DateField(null=True,blank=True)
    pickup_time = models.TimeField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    package_weight = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    number_of_packages = models.IntegerField(null=True,blank=True)

    # pickup address details
    sender_name = models.CharField(max_length=254,null=True,blank=True)
    sender_address = models.TextField(null=True,blank=True)
    sender_city = models.CharField(max_length=254,null=True,blank=True)
    sender_pincode = models.IntegerField(null=True,blank=True)
    sender_state = models.CharField(max_length=254,null=True,blank=True)
    sender_country = models.CharField(max_length=254,null=True,blank=True)
    sender_contact_no = models.CharField(max_length=100,null=True,blank=True)

    # delivery address details
    receiver_name = models.CharField(max_length=254,null=True,blank=True)
    receiver_address = models.TextField(null=True,blank=True)
    receiver_city = models.CharField(max_length=254,null=True,blank=True)
    receiver_pincode = models.IntegerField(null=True,blank=True)
    receiver_state = models.CharField(max_length=254,null=True,blank=True)
    receiver_country = models.CharField(max_length=254,null=True,blank=True)
    receiver_contact_no = models.CharField(max_length=100,null=True,blank=True)

    is_confirmed = models.IntegerField(default=0,null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)


class ShipmentTracking(models.Model):
    shipment = models.OneToOneField(ShipmentBooking, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('packed', 'Packed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('arrived_at_destination_hub', 'Arrived at Destination Hub'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('canceled', 'Canceled'),
        ('delayed', 'Delayed'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')
    tracking_number = models.CharField(max_length=20, unique=True, editable=False,null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/',null=True, blank=True)
    current_location = models.CharField(max_length=254, null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    is_delivered = models.BooleanField(default=False)   
    delivery_date = models.DateField(null=True, blank=True)  
    is_returned = models.BooleanField(default=False)  
    return_reason = models.TextField(null=True, blank=True) 
    is_arrived = models.BooleanField(default=False)   
    destination_hub_arrival_date = models.DateField(null=True, blank=True)  
    return_processed_date = models.DateField(null=True, blank=True)  
    shipped_date = models.DateField(null=True, blank=True)  
    delivery_attempts = models.IntegerField(default=0)  
    delivery_notes = models.TextField(null=True, blank=True)  
    status_history = models.JSONField(default=list, blank=True)  

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = str(uuid.uuid4()).replace('-', '')[:20]
        
        qrcode_img = qrcode.make(self.tracking_number)
        buffer = BytesIO()
        qrcode_img.save(buffer)
        self.qr_code.save(f'qrcode_{self.tracking_number}.png', File(buffer), save=False)
        if self.pk:
            old_instance = ShipmentTracking.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                self.status_history.append({
                    'status': self.status,
                    'timestamp': self.last_updated.isoformat()
                })


        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.shipment.booking_order_number} - {self.status}'





class CustomerIssues(models.Model):
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length = 254,null=True,blank=True)
    contact_number = models.CharField(max_length=100,null=True,blank=True)
    issues = models.TextField(null=True,blank=True)
    response = models.TextField(null=True,blank=True)
    action_taken = models.BooleanField(default=0,null=True,blank=True)

class OrderQueries(models.Model):
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    tracking_number = models.CharField(max_length=100,null=True,blank=True)
    queries = models.TextField(null=True,blank=True)
    response = models.TextField(null=True,blank=True)
    action_taken = models.BooleanField(default=0,null=True,blank=True)