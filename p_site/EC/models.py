from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # price を日本円（整数：円単位）で保存する
    price = models.PositiveIntegerField()  # 例: 1000 = ¥1,000
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
