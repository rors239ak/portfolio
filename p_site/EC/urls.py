from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product_list/', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
