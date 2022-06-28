from django.contrib import admin
from .models import Product, Brand, Images, Animal, ProductType, ProductOptions, Info, Article


class BrandAdmin(admin.ModelAdmin):
    """Бренды"""
    list_display = 'name',
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
    # list_display = 'title', 'animals', 'body_description', 'date_added', 'time_read', 'is_active',
    # list_editable = 'is_active',
    # list_filter = 'animals', 'time_read', 'is_active',
    # search_fields = 'title', 'body_description',
    list_per_page = 20


admin.site.register(Article, ArticleAdmin)


class ProductOptionsAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    # list_display = 'product', 'price', 'size', 'count', 'is_active',
    # list_editable = 'price', 'size', 'count', 'is_active',
    # list_filter = 'product', 'size', 'count', 'is_active',
    list_per_page = 20


admin.site.register(ProductOptions, ProductOptionsAdmin)



class ProductAdmin(admin.ModelAdmin):
    """Вариант фасовки"""
    # list_display = 'name',  'unit', 'date_added', 'animal', 'brand', 'is_active',
    # list_editable = 'is_active',
    # list_filter = 'date_added', 'animal', 'brand', 'is_active',
    list_per_page = 20


admin.site.register(Product, ProductAdmin)






# class ProductAdmin(admin.ModelAdmin):
#     """Товары магазина"""
#     list_display = 'name', 'description', 'unit', 'product_type', 'animal', 'brand', 'is_active',
#     # list_editable = 'name', 'published',
#     # list_display_links = 'title',
#     # list_filter = 'brands', 'volumes', 'type',
#     # search_fields = 'title', 'body_description',
#     list_per_page = 20
#
#
# admin.site.register(Product, ProductAdmin)


# class ProductImagesAdmin(admin.StackedInline):
#     model = Images
#
#
# @admin.register(Product)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [ProductImagesAdmin]
#
#     class Meta:
#         model = Product
#
#
# @admin.register(Images)
# class PostImageAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(Animal)
# admin.site.register(ProductType)
# admin.site.register(ProductOptions)
