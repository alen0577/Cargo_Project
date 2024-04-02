from django.db import models


# Create your models here.


# model for client testimonials
class Testimonials(models.Model):
    client_name = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)
    image = models.ImageField(null=True,blank = True,upload_to = 'image/testimonials') 
    position = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True,blank=True)


# model for current openings
class Currentopenings(models.Model):
    job_title = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)
    job_location = models.CharField(max_length=255,null=True,blank=True)
    job_type = models.CharField(max_length=255,null=True,blank=True)
    experience = models.CharField(max_length=255,null=True,blank=True)
    responsibilities = models.TextField(null=True,blank=True)
    requirements = models.TextField(null=True,blank=True)
    apply_email = models.EmailField(max_length = 254,null=True,blank=True)