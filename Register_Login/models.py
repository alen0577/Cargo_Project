from django.db import models

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
    admin_approval = models.IntegerField(default=0,null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)

