from django.db import models
from Admin.models import City

# Create your models here.

class CargoTeam(models.Model):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length = 254,null=True,blank=True)
    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True) 
    designation = models.CharField(max_length=255,null=True,blank=True)
    Joining_date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=254,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    state = models.CharField(max_length=254,null=True,blank=True)
    country = models.CharField(max_length=254,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    profile_picture = models.ImageField(null=True,blank = True,upload_to = 'image/profile_picture')
    admin_approval = models.IntegerField(default=0,null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)
    work_center = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
