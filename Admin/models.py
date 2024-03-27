from django.db import models

# Create your models here.


# model for client testimonials
class Testimonials(models.Model):
    client_name = models.CharField(max_length=255,null=True,blank=True)
    position = models.CharField(max_length=255,null=True,blank=True),
    testimonial_content=models.TextField(null=True,blank=True),
    is_active=models.BooleanField(default=1,null=True,blank=True)
