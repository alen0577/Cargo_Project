from django.db import models


# Create your models here.

# model for cargo services
class Services(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(null=True,blank = True,upload_to = 'image/services') 
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=1,null=True,blank=True)


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


# model for job applications
class JobApplications(models.Model):
    applied_for = models.ForeignKey(Currentopenings, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(max_length = 254,null=True,blank=True)
    contact_number = models.CharField(max_length=100,null=True,blank=True)
    resume = models.FileField(upload_to='Job_Applications/', max_length=255,)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    is_shortlisted = models.BooleanField(default=0,null=True,blank=True)

   
# model for service locations

class Country(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class State(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class City(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class ServiceLocation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    operating_hours = models.CharField(max_length=255, null=True, blank=True)
    service_type = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    

    
   