from django.urls import path
from . import views

urlpatterns = [
    path('api/cart/', views.cart_api, name='cart_api'),
    path('api/cart/add/', views.cart_add, name='cart_add'),
    path('api/cart/update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('customize/', views.customize_order, name='customize_order'),
]