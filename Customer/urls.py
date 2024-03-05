from django.urls import path
from . import views

urlpatterns = [
    path('book-pickup/', views.booking_request, name='booking_request'),
]