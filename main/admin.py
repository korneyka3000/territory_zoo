from django.contrib import admin

from .models import Product, Animal, Brand, ProductType, ProductOptions, Images


class ProductImagesAdmin(admin.StackedInline):
    model = Images

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]

    class Meta:
        model = Product

@admin.register(Images)
class PostImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Animal)
admin.site.register(Brand)
admin.site.register(ProductType)
admin.site.register(ProductOptions)
