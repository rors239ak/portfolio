from django.contrib import admin
from .models import Product, Category, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'owner')
    search_fields = ('name', 'description', 'owner__username')

    def _remove_images(self, obj):
        if hasattr(obj, 'images'):
            for img in list(obj.images.all()):
                try: img.image.delete(save=False)
                except Exception: pass
                img.delete()
        if getattr(obj, 'photo', None):
            try: obj.photo.delete(save=False)
            except Exception: pass

    def delete_model(self, request, obj):
        self._remove_images(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self._remove_images(obj)
        super().delete_queryset(request, queryset)
