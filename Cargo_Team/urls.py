from django.urls import path
from . import views

urlpatterns = [
    path('team-dashboard/',views.team_dashboard,name='team_dashboard'),  
    path('team-profile/',views.team_profile,name='team_profile'),
    path('update-team-profile/',views.edit_team_profile,name='edit_team_profile'),
    path('order-booking',views.order_booking,name='order_booking'),
    path('order-requests/',views.order_requests,name='order_requests'),
    path('order-request/<int:pk>/',views.order_request_details,name='order_request_details'),
    path('order-approval/<int:pk>/',views.order_approval,name='order_approval'),
    path('order-rejection/<int:pk>/',views.order_rejection,name='order_rejection'),
    path('pickup-orders/',views.pickup_orders,name='pickup_orders'),
    path('pickup-order/<int:pk>/',views.pickup_order_details,name='pickup_order_details'),
    path('edit-pickup-order/<int:pk>/',views.edit_pickup_order_details,name='edit_pickup_order_details'),
    path('rejected-orders/',views.rejected_orders,name='rejected_orders'), 
    path('customer-support/',views.customer_support,name='customer_support'), 
    path('pending-issues/',views.pending_issues,name='pending_issues'), 
    path('solved-issues/',views.solved_issues,name='solved_issues'), 
]