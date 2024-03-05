from django.db import models
import uuid

# Create your models here.

# Shipment booking model

class ShipmentBooking(models.Model):
    tracking_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length = 254, null=True, blank=True)
    contact_number = models.IntegerField()
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
    pickup_date = models.DateField()
    pickup_time = models.TimeField()