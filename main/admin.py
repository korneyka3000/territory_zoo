from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Product, Brand, Animal, Category, ProductOptions
from .resources import ProductAdminResource, AnimalAdminResource, BrandAdminResource



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
# 
class ProductOptionsAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    list_display = 'article_number', 'product', 'price', 'size', 'stock_balance', 'is_active',
    list_editable = 'price', 'size', 'stock_balance', 'is_active',
    list_filter = 'product', 'size', 'stock_balance', 'is_active',
    list_per_page = 20


admin.site.register(ProductOptions, ProductOptionsAdmin)


@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    list_display = 'name', 'image_img'
    search_fields = 'name',
    list_per_page = 20
    resource_class = AnimalAdminResource

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    list_display = 'name', 'image_img'
    search_fields = 'name',
    list_per_page = 20
    resource_class = BrandAdminResource

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = 'name', 'brand', 'image_img', 'date_added', 'is_active', 'product_options',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animal', 'brand', 'is_active',
    list_per_page = 20
    exclude = ('unique_name',)
    resource_class = ProductAdminResource

    def image_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80">')
        else:
            return 'Нет изображения'

    image_img.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории товара"""
    list_display = 'name', 'is_active',
    list_editable = 'is_active',
