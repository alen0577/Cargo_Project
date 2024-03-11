from django.urls import path
from . import views

urlpatterns = [
    path('book/shipment-order/', views.booking_request, name='booking_request'),
    path('pickup/', views.home_pickup_booking, name='home_pickup_booking'),
]