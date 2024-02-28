from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargo_home, name='cargo_home'),
    path('Cargo/aboutus', views.aboutus, name='aboutus'),
]