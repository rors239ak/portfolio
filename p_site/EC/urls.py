from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('products/new/', views.create_product, name='product_create'),  # 追加
]
