from django.urls import path
from . import views

urlpatterns = [
    path('executive-dashboard/',views.executive_dashboard,name='executive_dashboard'), 
    path('executive-profile/',views.executive_profile,name='executive_profile'),
    path('update-executive-profile/',views.edit_executive_profile,name='edit_executive_profile'),
    path('shipment-status/update/',views.shipment_status_update,name='shipment_status_update'),
    
]