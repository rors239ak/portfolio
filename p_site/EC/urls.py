from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_products/', views.create_product, name='product_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
