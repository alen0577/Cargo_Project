from django.urls import path
from . import views

urlpatterns = [
    path('book/shipment-order/', views.booking_request, name='booking_request'),
    path('pickup/', views.home_pickup_booking, name='home_pickup_booking'),
    path('dropoff/', views.shipping_center_booking, name='shipping_center_booking'),
    path('booking-details/<uuid:pk>', views.booking_details, name='booking_details'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]