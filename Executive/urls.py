from django.urls import path
from . import views

urlpatterns = [
    path('executive-dashboard/',views.executive_dashboard,name='executive_dashboard'), 
    path('executive-profile/',views.executive_profile,name='executive_profile'),
    path('update-executive-profile/',views.edit_executive_profile,name='edit_executive_profile'),

    path('shipment-status/update/',views.shipment_status_update,name='shipment_status_update'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
    path('all-shipment-orders/',views.all_shipment_orders,name='all_shipment_orders'),

    path('executive-return-management/',views.executive_return_management,name='executive_return_management'), 
    path('return-status/update/',views.return_shipment_status,name='return_shipment_status'),
    path('update-return-order-status/', views.update_return_order_status, name='update_return_order_status'),
    path('all-return-orders/',views.all_return_orders,name='all_return_orders'),


    path('order-queries/',views.query_section,name='query_section'),
    path('pending-queries/',views.pending_queries,name='pending_queries'),
    path('query-action-taken/<int:pk>/',views.query_action_taken,name='query_action_taken'),
    path('all-queries/',views.all_queries,name='all_queries'),
    
]