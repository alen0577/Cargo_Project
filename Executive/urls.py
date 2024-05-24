from django.urls import path
from . import views

urlpatterns = [
    path('executive-dashboard/',views.executive_dashboard,name='executive_dashboard'), 
    path('executive-profile/',views.executive_profile,name='executive_profile'),
    
]