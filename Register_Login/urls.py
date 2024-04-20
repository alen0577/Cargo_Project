from django.urls import path
from . import views

urlpatterns = [
    # login url section
    path('login-page/', views.login_page, name='login_page'),
    path('login-save/', views.login_save, name='login_save'),

    # register url section
    path('registration-page/',views.register_page,name='register_page'),
    path('team/registration',views.team_register,name='team_register'),

    # logout url section
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path('user-logout',views.logout,name='logout'),

]