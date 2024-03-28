from django.urls import path
from . import views

urlpatterns = [
    # login url section
    path('login-page/', views.login_page, name='login_page'),
    path('login-save/', views.login_save, name='login_save'),

    # logout url section
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    # path('User-Logout',views.logout,name='logout'),

]