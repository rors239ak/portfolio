from django.shortcuts import render
from django.db.models import Q
from .models import Product

def index(request):
    q = request.GET.get('q', '').strip()
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
    else:
        products = None
    return render(request, 'EC/index.html', {'products': products, 'q': q})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'EC/product_list.html', {"products": products})
