from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Product, Brand, Animal, Category, ProductOptions, ProductImage, Article, Comments, InfoShop
from .resources import ProductAdminResource, AnimalAdminResource, BrandAdminResource


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


class ProductImageInline(admin.TabularInline):
    """Изображение товара"""
    model = ProductImage
    extra = 2
    readonly_fields = 'preview',

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')

    preview.short_description = 'Превью изображения'


@admin.register(Category)
class Category(ImportExportModelAdmin):
    """Категории товара"""
    list_display = 'name', 'is_active', 'count_prod',
    list_editable = 'is_active',


class ProductOptionsInline(admin.TabularInline):
    """Вариант фасовки"""
    model = ProductOptions
    extra = 2


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    """Товары магазина"""
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '90'})}}

    fieldsets = (
        ('ОСНОВНЫЕ ДАННЫЕ', {'fields': ('name', 'brand', 'animal', 'category',)}),
        ('ИНФОРМАЦИЯ О ТОВАРЕ', {'fields': ('description', 'features', 'composition', 'additives', 'analysis',)}),
    )
    list_display = 'name', 'brand', 'category', 'date_added', 'is_active', 'product_options',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animal', 'brand', 'category', 'is_active',
    exclude = 'unique_name',
    resource_class = ProductAdminResource
    inlines = [ProductOptionsInline, ProductImageInline]
    list_per_page = 20


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Полезные статьи"""
    list_display = 'title', 'animals', 'image_img', 'body_description', 'date_added', 'time_read', 'is_active',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animals', 'time_read', 'is_active',
    search_fields = 'title', 'body_description',
    list_per_page = 20
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


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Отзыв о магазине"""
    list_display = 'name_author', 'body_description', 'phone_number', 'date_added', 'published',
    list_editable = 'published',
    list_filter = 'date_added', 'published',
    list_per_page = 20


@admin.register(InfoShop)
class InfoShopAdmin(admin.ModelAdmin):
    """Информация о магазине"""
    list_display = 'address', 'time_weekdays', 'time_weekend', 'phone_number', 'published',
    list_editable = 'time_weekdays', 'time_weekend', 'phone_number', 'published',

def status_colored(self, obj):
    color = 'yellow'
    if obj.status == 'Closed':
        color = 'green'
        return format_html(

            '<b style="background:{};">{}</b>',
            color,
            obj.status
                       )
    elif obj.status =='In Progress':
        color = 'yellow'
        return format_html(

            '<b style="background:{};">{}</b>',
            color,
            obj.status
                       )

    # else obj.status =='Needs Info':
    #     color = 'orange'
    #     return format_html(
    #
    #         '<b style="background:{};">{}</b>',
    #         color,
    #         obj.status
    #                    )

status_colored.admin_order_field = 'closed'

