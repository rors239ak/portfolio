from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Max
from django.core.paginator import Paginator
from .models import Product, Category, ProductImage   # ProductImage を追加
from .forms import ProductForm, SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import path
from . import views
import hashlib
import time
from django.http import JsonResponse, HttpResponseForbidden
from django.db import transaction, IntegrityError
from django.views.decorators.http import require_POST

#トップページ
@login_required
def index(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    price_min = request.GET.get('price_min', '').strip()
    price_max = request.GET.get('price_max', '').strip()
    sort = request.GET.get('sort', 'newest')  # 追加: ソートキー取得

    qs = Product.objects.all().select_related('category', 'owner')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category_id:
        qs = qs.filter(category_id=category_id)
    if price_min:
        try:
            qs = qs.filter(price__gte=int(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            qs = qs.filter(price__lte=int(price_max))
        except ValueError:
            pass

    # ソート適用
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'oldest':
        qs = qs.order_by('id')
    elif sort == 'name_asc':
        qs = qs.order_by('name')
    elif sort == 'name_desc':
        qs = qs.order_by('-name')
    else:
        qs = qs.order_by('-id')  # newest (デフォルト)

    paginator = Paginator(qs, 16)  # 変更: 1ページあたり16件（4列×4行）
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    # ページネーション用に現在のクエリ（page を除く）を組み立て
    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')
    querystring = params.urlencode()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
        'price_options': [0,500,1000,2000,5000,10000],
        'selected_min': price_min,
        'selected_max': price_max,
        'total_count': qs.count(),
        'is_paginated': page_obj.has_other_pages(),
        'sort': sort,
        'querystring': querystring,
    }
    return render(request, 'EC/index.html', context)


#商品作成ページ
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # セッション重複チェック用 fingerprint を作る
            name = form.cleaned_data.get('name','') or ''
            price = str(form.cleaned_data.get('price','') or '')
            desc = form.cleaned_data.get('description','') or ''
            photos = request.FILES.getlist('photos')
            files_sig = '|'.join([f.name for f in photos])
            fp_src = f"{request.user.pk}|{name}|{price}|{desc}|{files_sig}"
            fp = hashlib.sha256(fp_src.encode('utf-8')).hexdigest()

            last_fp = request.session.get('last_product_fp')
            last_time = request.session.get('last_product_time', 0)

            # 10秒以内に同じ内容で再送があれば既存作成扱い（重複防止）
            if last_fp == fp and time.time() - float(last_time) < 10:
                existing_pk = request.session.get('last_product_pk')
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'product': {'id': existing_pk}}, status=200)
                return redirect('product_detail', pk=existing_pk)

            # 実際の作成処理
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            errors = []
            for i, f in enumerate(photos[:15]):
                try:
                    ProductImage.objects.create(product=product, image=f, order=product.images.count() + i)
                except Exception as e:
                    errors.append(str(e))

            # images の先頭を main photo に同期
            if product.images.exists():
                first = product.images.first()
                if first and first.image:
                    product.photo = first.image
                    product.save()

            # セッションに保存して短時間の重複を防ぐ
            request.session['last_product_fp'] = fp
            request.session['last_product_time'] = str(time.time())
            request.session['last_product_pk'] = product.pk

            # AJAX 応答
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                if errors:
                    return JsonResponse({'success': False, 'errors': errors}, status=500)
                return JsonResponse({
                    'success': True,
                    'product': {
                        'id': product.pk,
                        'name': product.name,
                        'price': product.price,
                        'photo_url': product.photo.url if product.photo else ''
                    }
                })
            return redirect('product_detail', pk=product.pk)
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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'EC/product_detail.html', {'product': product})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # セッション重複チェック用 fingerprint（編集用）
            name = form.cleaned_data.get('name','') or ''
            price = str(form.cleaned_data.get('price','') or '')
            desc = form.cleaned_data.get('description','') or ''
            photos = request.FILES.getlist('photos')
            files_sig = '|'.join([f.name for f in photos])
            fp_src = f"edit|{request.user.pk}|{product.pk}|{name}|{price}|{desc}|{files_sig}"
            fp = hashlib.sha256(fp_src.encode('utf-8')).hexdigest()

            last_fp = request.session.get('last_edit_fp')
            last_time = request.session.get('last_edit_time', 0)

            # 10秒以内に同じ内容で再送があれば処理スキップ（重複防止）
            if last_fp == fp and time.time() - float(last_time) < 10:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'product': {'id': product.pk}}, status=200)
                return redirect('product_detail', pk=product.pk)

            # 実際の更新処理
            form.save()
            photos = request.FILES.getlist('photos')
            errors = []
            existing = product.images.count()
            for i, f in enumerate(photos[: max(0, 15 - existing)]):
                try:
                    ProductImage.objects.create(product=product, image=f, order=existing + i)
                except Exception as e:
                    errors.append(str(e))

            # images の先頭を main photo に同期
            if product.images.exists():
                first = product.images.first()
                product.photo = first.image if first and first.image else None
            else:
                product.photo = None
            product.save()

            # セッションに fingerprint 保存
            request.session['last_edit_fp'] = fp
            request.session['last_edit_time'] = str(time.time())
            request.session.modified = True

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                if errors:
                    return JsonResponse({'success': False, 'errors': errors}, status=500)
                return JsonResponse({
                    'success': True,
                    'product': {
                        'id': product.pk,
                        'name': product.name,
                        'price': product.price,
                        'photo_url': product.photo.url if product.photo else ''
                    }
                })
            return redirect('product_detail', pk=product.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ProductForm(instance=product)

    return render(request, 'EC/product_create.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 追加画像（ProductImage など）がある場合は先に削除して物理ファイルも消す
                if hasattr(product, 'images'):
                    for img in list(product.images.all()):
                        try:
                            img.image.delete(save=False)
                        except Exception:
                            pass
                        img.delete()

                # main photo のファイルも削除（モデルに photo フィールドがある場合）
                try:
                    if getattr(product, 'photo', None):
                        product.photo.delete(save=False)
                except Exception:
                    pass

                # 最後に product を削除
                product.delete()

            return redirect('index')
        except IntegrityError:
            # 外部キー制約などで削除できない場合のフォールバック表示
            return render(request, 'EC/product_confirm_delete.html', {
                'product': product,
                'error': '削除に失敗しました（関連データの制約）。サーバログを確認してください。'
            })

    return render(request, 'EC/product_confirm_delete.html', {'product': product})

@login_required
@require_POST
def delete_product_image(request, pk, img_pk):
    """
    編集画面からの AJAX POST による画像削除。
    URL: /EC/product/<pk>/image/<img_pk>/delete/
    """
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden()

    img = get_object_or_404(ProductImage, pk=img_pk, product=product)
    try:
        # 物理ファイルを安全に削除
        try:
            img.image.delete(save=False)
        except Exception:
            pass
        img.delete()

        # 削除後に product.photo を images.first() に再同期（無ければ None）
        if product.images.exists():
            first = product.images.first()
            product.photo = first.image if first and first.image else None
        else:
            product.photo = None
        product.save()

        new_main = product.photo.url if product.photo else ''
        return JsonResponse({'success': True, 'img_pk': img_pk, 'new_main_url': new_main})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def delete_product_images_bulk(request, pk):
    """
    編集画面からの一括削除（AJAX）
    POST: img_pks[]=1 (複数)
    """
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden()

    # リストは POST の複数値または JSON どちらでも受け取る
    img_pks = request.POST.getlist('img_pks[]') or request.POST.getlist('img_pks') or []
    # JSON support
    if not img_pks:
        try:
            import json
            body = json.loads(request.body.decode() or '{}')
            img_pks = body.get('img_pks', [])
        except Exception:
            img_pks = img_pks

    deleted = []
    errors = []
    try:
        with transaction.atomic():
            for s in img_pks:
                try:
                    img = ProductImage.objects.get(pk=int(s), product=product)
                except ProductImage.DoesNotExist:
                    continue
                # delete file
                try:
                    img.image.delete(save=False)
                except Exception:
                    pass
                img.delete()
                deleted.append(img.pk)

            # 同期 main photo
            if product.images.exists():
                first = product.images.first()
                product.photo = first.image if first and first.image else None
            else:
                product.photo = None
            product.save()
        return JsonResponse({'success': True, 'deleted': deleted, 'new_main_url': product.photo.url if product.photo else ''})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def account_dashboard(request):
    """
    マイページ：ログインユーザーの出品一覧をページネーションで表示
    """
    qs = Product.objects.filter(owner=request.user).order_by('-pk')
    pager = Paginator(qs, 12)
    page_num = request.GET.get('page', 1)
    products = pager.get_page(page_num)
    return render(request, 'EC/account_dashboard.html', {'products': products})


