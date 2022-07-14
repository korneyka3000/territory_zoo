from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Product, Animal, Brand, Category, ProductOptions


class ForeignKeyWidgetWithCreation(ForeignKeyWidget):
    def __init__(self, model, field="pk", create=False, **kwargs):
        self.model = model
        self.field = field
        self.create = create
        super(ForeignKeyWidgetWithCreation, self).__init__(model, field=field, **kwargs)

    def clean(self, value, **kwargs):
        print(value)
        if not value:
            return None
        if self.create:
            self.model.objects.get_or_create(**{self.field: value})
        val = super(ForeignKeyWidgetWithCreation, self).clean(value, **kwargs)
        return self.model.objects.get(**{self.field: val}) if val else None


class ProductAdminResource(resources.ModelResource):
    animal = fields.Field(column_name='animal', attribute='animal',
                          widget=ManyToManyWidget(Animal, field='name', separator=', '))
    category = fields.Field(column_name='category', attribute='category',
                            widget=ForeignKeyWidgetWithCreation(Category, field='name', create=True))
    brand = fields.Field(column_name='brand', attribute='brand',
                         widget=ForeignKeyWidgetWithCreation(Brand, field='name', create=True))
    options = fields.Field(column_name='product', attribute='options',
                           widget=ForeignKeyWidgetWithCreation(ProductOptions, field='product_id', create=True))

    class Meta:
        model = Product
        fields = ('id', 'name', 'animal', 'category', 'brand', 'options',)
        export_order = ('id', 'name', 'animal', 'category', 'brand', 'options',)  # порядок экспорта полей


class AnimalAdminResource(resources.ModelResource):
    class Meta:
        model = Animal
        fields = ('id', 'name',)


class BrandAdminResource(resources.ModelResource):
    class Meta:
        model = Brand
        fields = ('id', 'name',)


class CategoryAdminResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name',)
