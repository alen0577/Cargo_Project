from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # testimonial urls
    path('service-central/', views.service_section, name='service_section'),
    path('service-save/', views.service_save, name='service_save'),
    path('service-edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('service-delete/<int:pk>/', views.service_delete, name='service_delete'),

    # testimonial urls
    path('testimonial-hub/', views.testimonial_section, name='testimonial_section'),
    path('testimonial-save/', views.testimonial_save, name='testimonial_save'),
    path('testimonial-edit/<int:pk>/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonial-delete/<int:pk>/', views.testimonial_delete, name='testimonial_delete'),

    # career section urls
    path('career-corner/', views.career_section, name='career_section'),
    path('currentopening-save/', views.current_opening_save, name='current_opening_save'),
    path('opening-edit/<int:pk>/', views.opening_edit, name='opening_edit'),
    path('opening-delete/<int:pk>/', views.opening_delete, name='opening_delete'),
    path('applications/<int:pk>/', views.application_lists, name='application_lists'),
    path('view-resume/<int:pk>/', views.view_resume, name='view_resume'),
    path('download-resume/<int:pk>/', views.download_resume, name='download_resume'),

    # cargo team section urls
    path('cargo-team/', views.cargo_team, name='cargo_team'),
    path('login-requests/', views.login_requests, name='login_requests'),
    path('accept-request/<int:pk>/', views.accept_request, name='accept_request'),
    path('cancel-request/<int:pk>/', views.cancel_request, name='cancel_request'),
    path('approved-requests/', views.approved_requests, name='approved_requests'),
    path('rejected-requests/', views.rejected_requests, name='rejected_requests'),
    path('member-details/', views.member_details, name='member_details'),
    path('team-members/', views.team_members, name='team_members'),
    path('executive-members/', views.executive_members, name='executive_members'),

    # cargo service location management urls
    path('location-hub/', views.location_hub, name='location_hub'),
    path('add-country/', views.add_country, name='add_country'),
    path('add-state/', views.add_state, name='add_state'),
    path('add-city/', views.add_city, name='add_city'),
    path('add-location/', views.add_location, name='add_location'),
    path('edit-location/<int:pk>/', views.edit_location, name='edit_location'),
    path('delete-country/<int:pk>/', views.delete_country, name='delete_country'),
    path('delete-state/<int:pk>/', views.delete_state, name='delete_state'),
    path('delete-city/<int:pk>/', views.delete_city, name='delete_city'),
    path('delete-location/<int:pk>/', views.delete_location, name='delete_location'),
    path('active-country/<int:pk>/', views.active_country, name='active_country'),
    path('inactive-country/<int:pk>/', views.inactive_country, name='inactive_country'),
    path('active-state/<int:pk>/', views.active_state, name='active_state'),
    path('inactive-state/<int:pk>/', views.inactive_state, name='inactive_state'),
    path('active-city/<int:pk>/', views.active_city, name='active_city'),
    path('inactive-city/<int:pk>/', views.inactive_city, name='inactive_city'),
    path('active-location/<int:pk>/', views.active_location, name='active_location'),
    path('inactive-location/<int:pk>/', views.inactive_location, name='inactive_location'),






]