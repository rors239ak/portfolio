from django.shortcuts import render, redirect
from django.db.models import Q, Max
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm, SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.http import JsonResponse

#トップページ
@login_required
def index(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    price_min = request.GET.get('price_min', '').strip()
    price_max = request.GET.get('price_max', '').strip()

    products_qs = Product.objects.all().order_by('-created_at')

    if q:
        products_qs = products_qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if category_id:
        try:
            products_qs = products_qs.filter(category_id=int(category_id))
        except ValueError:
            pass

    try:
        if price_min != '':
            products_qs = products_qs.filter(price__gte=int(price_min))
        if price_max != '':
            products_qs = products_qs.filter(price__lte=int(price_max))
    except ValueError:
        pass

    # 全件数（フィルタ後の総数）
    total_count = products_qs.count()

    # ページング（10件ごと）
    paginator = Paginator(products_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 現在のクエリ文字列（page を除外）を作る（ページリンクで再利用）
    qd = request.GET.copy()
    if 'page' in qd:
        qd.pop('page')
    querystring = qd.urlencode()

    categories = Category.objects.all()

    # 価格選択肢は既存ロジックを維持（必要なら view 内で作成）
    max_price = Product.objects.aggregate(max=Max('price'))['max'] or 0
    step = 1000
    max_bucket = ((max_price // step) + 2) * step
    price_options = list(range(0, max_bucket + 1, step))

    context = {
        'products': page_obj,      # テンプレでは page_obj をループ代わりに利用可
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'total_count': total_count,
        'q': q,
        'categories': categories,
        'price_options': price_options,
        'selected_category': category_id,
        'selected_min': price_min,
        'selected_max': price_max,
        'querystring': querystring,
    }
    return render(request, 'EC/index.html', context)


#商品作成ページ
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # owner を紐付けて保存
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            # Ajax (fetch) の場合は JSON を返す
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'category': product.category.name if product.category else '',
                        'photo_url': product.photo.url if product.photo else '',
                        'description': product.description,
                        'owner': product.owner.username if product.owner else '',
                    }
                })
            return render(request, 'EC/product_create.html', {'product': product})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ProductForm()
    return render(request, 'EC/product_create.html', {'form': form})

#会員登録ビュー
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('login')  # 登録後にログインページへ
    else:
        form = SignupForm()
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


