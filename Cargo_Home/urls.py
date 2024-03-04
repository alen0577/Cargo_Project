from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargo_home, name='cargo_home'),
    path('About-Us/', views.aboutus, name='aboutus'),
    path('Contact-Us/', views.contactus, name='contactus'),
    path('Services', views.services, name='services'),
    path('Careers/', views.careers, name='careers'),
    
]