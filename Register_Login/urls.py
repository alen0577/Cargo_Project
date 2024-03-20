from django.urls import path
from . import views

urlpatterns = [
    path('login-page/', views.login_page, name='login_page'),
    path('login-save/', views.login_save, name='login_save'),
]