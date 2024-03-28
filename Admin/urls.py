from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('testimonial-hub/', views.testimonial_section, name='testimonial_section'),
    path('testimonial-save/', views.testimonial_save, name='testimonial_save'),
]