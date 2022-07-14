from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Product, Brand, Animal, Category, ProductOptions, ProductImage, Article, Comments
from .resources import ProductAdminResource, AnimalAdminResource, BrandAdminResource

admin.site.site_header = 'Территория ZOO'  # Надпись в админке сайта


# from django.http import HttpResponseRedirect
# from django.conf.urls import url
# from .models import LoginMonitor
# from .import_custom import ImportCustom
#

class ProductImageInline(admin.TabularInline):
    """Изображение товара"""
    model = ProductImage
    extra = 2
    readonly_fields = 'preview',

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')

    preview.short_description = 'Превью изображения'


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
    list_display = 'name', 'button', 'brand', 'category', 'date_added', 'is_active', 'product_options',
    list_editable = 'is_active',
    list_filter = 'date_added', 'animal', 'brand', 'category', 'is_active',
    exclude = 'unique_name',
    resource_class = ProductAdminResource
    radio_fields = {'category': admin.HORIZONTAL, 'brand': admin.HORIZONTAL}  # Отображаемые поля столбец, список
    inlines = [ProductOptionsInline, ProductImageInline]
    list_per_page = 20

    class ImportAdmin(admin.ModelAdmin):
        change_list_template = 'admin/change_list.html'  # Кнопка для загрузки товара

    def button(self, obj):  # Кнопка в самом товаре для редактирования
        # return mark_safe(f'<a class="button" >Добавить</a>')
        return mark_safe(f'<a href="localhost" class ="button"> Главная <a>')
    button.short_description = 'Ссылка на сайт'


    # change_list_template = "admin/monitor_change_list.html"
    # def get_urls(self):
    #     urls = super(ProductAdmin, self).get_urls().custom_urls = [url('^import/$', self.process_import, name='process_import'),]
    #     return urls
    # def process_import_btmp(self, request):
    #     import_custom = ImportCustom()
    #     count = import_custom.import_data()
    #     self.message_user(request, f"создано {count} новых записей")
    #     return HttpResponseRedirect("../")


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


@admin.register(Category)
class Category(ImportExportModelAdmin):
    """Категории товара"""
    list_display = 'name', 'is_active', 'count_prod',
    list_editable = 'is_active',


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

# @admin.register(InfoShop)
# class InfoShopAdmin(admin.ModelAdmin):
#     """Информация о магазине"""
#     list_display = 'address', 'time_weekdays', 'time_weekend', 'phone_number', 'published',
#     list_editable = 'time_weekdays', 'time_weekend', 'phone_number', 'published',
