from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_products/', views.create_product, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.edit_product, name='product_edit'),   # 追加
    path('product/<int:pk>/delete/', views.delete_product, name='product_delete'), # 追加
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('product/<int:pk>/image/<int:img_pk>/delete/', views.delete_product_image, name='product_image_delete'),
    path('product/<int:pk>/images/delete/', views.delete_product_images_bulk, name='product_images_delete_bulk'),
    path('account/', views.account_dashboard, name='account_dashboard'),
]
