from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import Product, Brand, Animal, Category, ProductOptions, ProductImage, Article, Comments, InfoShop, \
    Consultation, Customer, Order, OrderItem
from .resources import ProductAdminResource, AnimalAdminResource, BrandAdminResource

admin.site.site_header = 'Территория ZOO'  # Надпись в админке сайта


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
        ('ИНФОРМАЦИЯ О ТОВАРЕ',
         {'fields': ('popular', 'description', 'features', 'composition', 'additives', 'analysis',)}),
    )
    list_display = ('name', 'brand', 'category', 'date_added', 'popular', 'is_active', 'product_options',)
    list_editable = ('is_active', 'popular')
    list_filter = ('date_added', 'animal', 'brand', 'category', 'is_active', 'popular',)
    exclude = 'unique_name',
    resource_class = ProductAdminResource
    inlines = [ProductOptionsInline, ProductImageInline]
    list_per_page = 20

    # class ImportAdmin(admin.ModelAdmin):
    #     change_list_template = 'admin/change_list.html'  # Кнопка для загрузки товара
    # def button(self, obj):  # Кнопка в самом товаре для редактирования
    #     # return mark_safe(f'<a class="button" >Добавить</a>')
    #     return mark_safe(f'<a href="localhost" class ="button"> Главная <a>')
    # button.short_description = 'Ссылка на сайт'


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
    list_display = ('name_author', 'body_description', 'phone_number', 'date_added', 'published',)
    list_editable = ('published',)
    list_filter = ('date_added', 'published',)
    list_per_page = 20


@admin.register(InfoShop)
class InfoShopAdmin(admin.ModelAdmin):
    """Информация о магазине"""
    list_display = ('address', 'time_weekdays', 'time_weekend', 'phone_number',)  # 'published',
    list_editable = ('time_weekdays', 'time_weekend', 'phone_number',)  # 'published',

    def add_view(self, request):
        if request.method == "POST":
            if InfoShop.objects.count() >= 1:
                return HttpResponse("Только один адрес доступен, измените существующий")
        return super(InfoShopAdmin, self).add_view(request)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',)
    list_display_links = ('name', 'phone',)


# @admin.register(Order)
class OrderInlineAdmin(admin.TabularInline):
    model = Order


# @admin.register(OrderItem)
class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number',)
    list_display_links = ('customer_name',)
    # list_editable = ('customer_name', 'phone_number',)
    list_filter = ('customer_name', 'phone_number',)
    list_per_page = 20
    inlines = [OrderInlineAdmin]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'paid', 'created',)
    # list_display_links = ('paid', 'created',)
    list_editable = ('paid',)
    readonly_fields = ('created',)
    list_filter = ('customer', 'paid', 'created',)
    list_per_page = 20
    inlines = [OrderItemInlineAdmin]
