from django.urls import path
from . import views

urlpatterns = [
    path('team-dashboard/',views.team_dashboard,name='team_dashboard'),  
    path('team-profile/',views.team_profile,name='team_profile'),
    path('update-team-profile/',views.edit_team_profile,name='edit_team_profile'),

    path('order-booking',views.order_booking,name='order_booking'),
    path('order-booking-save',views.order_booking_save,name='order_booking_save'),

    path('order-requests/',views.order_requests,name='order_requests'),
    path('order-request/<int:pk>/',views.order_request_details,name='order_request_details'),
    path('order-approval/<int:pk>/',views.order_approval,name='order_approval'),
    path('order-rejection/<int:pk>/',views.order_rejection,name='order_rejection'),

    path('pickup-requests/',views.pickup_orders,name='pickup_orders'),
    path('pickup-request/<int:pk>/',views.pickup_order_details,name='pickup_order_details'),
    path('edit-pickup-order/<int:pk>/',views.edit_pickup_order_details,name='edit_pickup_order_details'),
    path('bill-request-approve/<int:pk>/',views.bill_request_approve,name='bill_request_approve'),

    path('bill-requests/',views.bill_requests,name='bill_requests'), 
    path('bill-request/<int:pk>/',views.bill_request_details,name='bill_request_details'), 

    path('all-orders/',views.all_orders,name='all_orders'),
    path('rejected-orders/',views.rejected_orders,name='rejected_orders'), 

    path('customer-support/',views.customer_support,name='customer_support'), 
    path('pending-issues/',views.pending_issues,name='pending_issues'), 
    path('solved-issues/',views.solved_issues,name='solved_issues'), 
]