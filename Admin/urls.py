from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # testimonial urls
    path('testimonial-hub/', views.testimonial_section, name='testimonial_section'),
    path('testimonial-save/', views.testimonial_save, name='testimonial_save'),
    path('testimonial-edit/<int:pk>/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonial-delete/<int:pk>/', views.testimonial_delete, name='testimonial_delete'),

    # career section urls
    path('career-corner/', views.career_section, name='career_section'),
]