from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Product, Brand, Animal, Category, ProductOptions, ProductImage
from .resources import ProductAdminResource, AnimalAdminResource, BrandAdminResource


@admin.register(ProductOptions)
class ProductOptionsAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    list_display = 'article_number', 'product', 'price', 'size', 'stock_balance', 'is_active',
    list_editable = 'price', 'size', 'stock_balance', 'is_active',
    list_filter = 'product', 'size', 'stock_balance', 'is_active',
    list_per_page = 20


@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    """Типы животных"""
    list_display = 'name', 'image_img', 'count_prod',
    search_fields = 'name',
    readonly_fields = 'preview',
    resource_class = AnimalAdminResource
    list_per_page = 20

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')

    preview.short_description = 'Превью изображения'


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    """Бренды товаров"""
    list_display = 'name', 'image_img', 'count_prod',
    search_fields = 'name',
    readonly_fields = 'preview',
    resource_class = BrandAdminResource
    list_per_page = 20

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')

    preview.short_description = 'Превью изображения'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Изображение товара"""
    list_display = 'image_img',
    readonly_fields = 'preview',

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')

    preview.short_description = 'Превью изображения'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    """Товары магазина"""
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '90'})}}
    list_display = 'name', 'brand', 'date_added', 'is_active', 'product_options',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animal', 'brand', 'is_active',
    exclude = 'unique_name',
    resource_class = ProductAdminResource
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Категории товара"""
    list_display = 'name', 'is_active', 'count_prod',
    list_editable = 'is_active',

#
#
# class InfoAdmin(admin.ModelAdmin):
#     """Информация о магазине"""
#     list_display = 'address', 'time_weekdays', 'time_weekend', 'phone_number', 'published',
#     list_editable = 'time_weekdays', 'time_weekend', 'phone_number', 'published',
#
#
# admin.site.register(Info, InfoAdmin)
#
#
# class ArticleAdmin(admin.ModelAdmin):
#     """Полезные статьи"""
#     list_display = 'title', 'animals', 'body_description', 'date_added', 'time_read', 'is_active',
#     list_editable = 'is_active',
#     list_filter = 'animals', 'time_read', 'is_active',
#     search_fields = 'title', 'body_description',
#     list_per_page = 20
#
#
# admin.site.register(Article, ArticleAdmin)
#
