from django.db import models
import uuid

# Create your models here.

# Shipment booking model

class ShipmentBooking(models.Model):

    # tracking code
    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Shipment type field
    shipment_type = models.CharField(max_length=30, default='Home Pickup')

    # customer details
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length = 254, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)

    # shipment details
    delivery_option_choices = [
        ('road', 'By Road'),
        ('air', 'By Air'),
        ('sea', 'By Sea')
    ]
    delivery_option = models.CharField(max_length=10, choices=delivery_option_choices, null=True, blank=True)
    delivery_type_choices = [
        ('normal', 'Normal'),
        ('speed', 'Speed')
    ]
    delivery_type = models.CharField(max_length=10, choices=delivery_type_choices, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    package_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    number_of_packages = models.IntegerField(null=True, blank=True)

    # pickup address details
    sender_name = models.CharField(max_length=254, null=True, blank=True)
    sender_address = models.TextField(null=True, blank=True)
    sender_city = models.CharField(max_length=254, null=True, blank=True)
    sender_pincode = models.IntegerField(null=True, blank=True)
    sender_state = models.CharField(max_length=254, null=True, blank=True)
    sender_country = models.CharField(max_length=254, null=True, blank=True)
    sender_contact_no = models.CharField(max_length=100, null=True, blank=True)

    # delivery address details
    receiver_name = models.CharField(max_length=254, null=True, blank=True)
    receiver_address = models.TextField(null=True, blank=True)
    receiver_city = models.CharField(max_length=254, null=True, blank=True)
    receiver_pincode = models.IntegerField(null=True, blank=True)
    receiver_state = models.CharField(max_length=254, null=True, blank=True)
    receiver_country = models.CharField(max_length=254, null=True, blank=True)
    receiver_contact_no = models.CharField(max_length=100, null=True, blank=True)

    is_confirmed = models.BooleanField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=0, null=True, blank=True)