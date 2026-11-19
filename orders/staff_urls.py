from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('store_pos'), name='staff_home'),
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('pos/', views.store_pos, name='store_pos'),
    path('dashboard/', views.sales_dashboard, name='sales_dashboard'),
]