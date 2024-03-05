from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargo_home, name='cargo_home'),
    path('about-us/', views.aboutus, name='aboutus'),
    path('contact-us/', views.contactus, name='contactus'),
    path('services', views.services, name='services'),
    path('careers/', views.careers, name='careers'),
    
]