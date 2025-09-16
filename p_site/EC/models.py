from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # カテゴリ
    description = models.TextField()
    # 写真（任意）
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)
    # 出品者（ユーザー）: 既存データ対応のため null=True にしておく
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    # price を日本円（整数：円単位）で保存する
    price = models.PositiveIntegerField()  # 例: 1000 = ¥1,000
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
