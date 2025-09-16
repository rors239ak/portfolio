from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.index, name='product_list'),  # product_list は index に統合
    path('products/new/', views.create_product, name='product_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
