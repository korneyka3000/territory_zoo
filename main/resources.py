from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Product, Animal, Brand, Category


class ProductAdminResource(resources.ModelResource):
    animal = fields.Field(column_name='animal', attribute='animal',
                          widget=ManyToManyWidget(Animal, field='name', separator=', '))
    category = fields.Field(column_name='category', attribute='category',
                            widget=ForeignKeyWidget(Category, field='name'))
    brand = fields.Field(column_name='brand', attribute='brand', widget=ForeignKeyWidget(Brand, field='name'))

    class Meta:
        model = Product
        fields = 'id', 'name', 'animal', 'category', 'brand'
        export_order = 'id', 'name', 'animal', 'category', 'brand'  # порядок экспорта полей


class AnimalAdminResource(resources.ModelResource):
    class Meta:
        model = Animal
        fields = 'id', 'name',


class BrandAdminResource(resources.ModelResource):
    class Meta:
        model = Brand
        fields = 'id', 'name',


class CategoryAdminResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = 'id', 'name',
