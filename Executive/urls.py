from django.urls import path
from . import views

urlpatterns = [
    path('executive-dashboard/',views.executive_dashboard,name='executive_dashboard'), 
    path('executive-profile/',views.executive_profile,name='executive_profile'),
    path('update-executive-profile/',views.edit_executive_profile,name='edit_executive_profile'),
    path('shipment-status/update/',views.shipment_status_update,name='shipment_status_update'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),

    path('order-queries/',views.query_section,name='query_section'),
    path('pending-queries/',views.pending_queries,name='pending_queries'),
    path('all-queries/',views.all_queries,name='all_queries'),
    
]