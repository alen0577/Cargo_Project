from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargo_home, name='cargo_home'),
    path('about-us/', views.aboutus, name='aboutus'),
    path('contact-us/', views.contactus, name='contactus'),
    path('customer-issues/', views.customer_issues, name='customer_issues'),
    path('services', views.services, name='services'),
    path('service-details/<int:pk>/', views.service_details, name='service_details'),
    path('careers/', views.careers, name='careers'),
    path('job-apply/', views.job_apply, name='job_apply'),

    
]