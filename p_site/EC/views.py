from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

#トップページ
@login_required
def index(request):
    q = request.GET.get('q', '').strip()
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
    else:
        products = None
    return render(request, 'EC/index.html', {'products': products, 'q': q})

#商品一覧ページ
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'EC/product_list.html', {"products": products})

#商品作成ページ
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'EC/product_create.html', {'form': form})

#会員登録ビュー
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録後にログインページへ
    else:
        form = UserCreationForm()
    return render(request, 'EC/signup.html', {'form': form})

# ログインビュー
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'EC/login.html', {'form': form})


