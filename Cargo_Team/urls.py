from django.urls import path
from . import views

urlpatterns = [
    path('team-dashboard/',views.team_dashboard,name='team_dashboard'),    
]