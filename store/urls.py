from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('wish_list/', views.wish_list, name='wish_list'),
    path('detail/<str:pk>', views.detail, name='detail'),
    path('checkout/', views.checkout, name='checkout'),


    path('add_Cart/', views.add_Cart, name='add_Cart'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),


    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('register/', views.register, name='register'),

    path('processorder/', views.processorder, name='processorder')
]