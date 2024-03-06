from django.db import models
import uuid

# Create your models here.

# Shipment booking model

class ShipmentBooking(models.Model):

    # tracking code
    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # customer details
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length = 254, null=True, blank=True)
    contact_number = models.IntegerField()

    # shipment details
    delivery_method_choices = [
        ('road', 'By Road'),
        ('air', 'By Air'),
        ('sea', 'By Sea')
    ]
    delivery_method = models.CharField(max_length=10, choices=delivery_method_choices)
    delivery_speed_choices = [
        ('normal', 'Normal'),
        ('speed', 'Speed')
    ]
    delivery_speed = models.CharField(max_length=10, choices=delivery_speed_choices)
    pickup_date = models.DateField(auto_now_add=True)
    pickup_time = models.TimeField(auto_now_add=True)
    package_weight = models.DecimalField(max_digits=5, decimal_places=5)
    number_of_packages = models.IntegerField()

    # pickup address details
    sender_name = models.CharField(max_length=254)
    sender_address = models.TextField()
    sender_city = models.CharField(max_length=254)
    sender_pincode = models.IntegerField()
    sender_state = models.CharField(max_length=254)
    sender_country = models.CharField(max_length=254)
    sender_contact_no = models.IntegerField()

    # delivery address details
    receiver_name = models.CharField(max_length=254)
    receiver_address = models.TextField()
    receiver_city = models.CharField(max_length=254)
    receiver_pincode = models.IntegerField()
    receiver_state = models.CharField(max_length=254)
    receiver_country = models.CharField(max_length=254)
    receiver_contact_no = models.IntegerField()