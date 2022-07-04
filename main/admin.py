from django.contrib import admin
from .models import Product, Brand, Animal, Category, ProductOptions, Info, Article


class BrandAdmin(admin.ModelAdmin):
    """Бренды"""
    list_display = 'id', 'name', 'count_prod',
    search_fields = 'name',
    list_per_page = 20


admin.site.register(Brand, BrandAdmin)


class AnimalAdmin(admin.ModelAdmin):
    """Животные"""
    list_display = 'name',
    search_fields = 'name',
    list_per_page = 20


admin.site.register(Animal, AnimalAdmin)


class InfoAdmin(admin.ModelAdmin):
    """Информация о магазине"""
    list_display = 'address', 'time_weekdays', 'time_weekend', 'phone_number', 'published',
    list_editable = 'time_weekdays', 'time_weekend', 'phone_number', 'published',


admin.site.register(Info, InfoAdmin)


class ArticleAdmin(admin.ModelAdmin):
    """Полезные статьи"""
    list_display = 'title', 'animals', 'body_description', 'date_added', 'time_read', 'is_active',
    list_editable = 'is_active',
    list_filter = 'animals', 'time_read', 'is_active',
    search_fields = 'title', 'body_description',
    list_per_page = 20


admin.site.register(Article, ArticleAdmin)


class ProductOptionsAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    list_display = 'product', 'price', 'size', 'count', 'is_active',
    list_editable = 'price', 'size', 'count', 'is_active',
    list_filter = 'product', 'size', 'count', 'is_active',
    list_per_page = 20


admin.site.register(ProductOptions, ProductOptionsAdmin)


class ProductAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    list_display = 'name', 'brand', 'body_description', 'unit', 'date_added', 'is_active',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animal', 'brand', 'is_active',
    list_per_page = 20


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """Категории товара"""
    list_display = 'name', 'is_active',
    list_editable = 'is_active',


admin.site.register(Category, CategoryAdmin)

