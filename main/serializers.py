from pprint import pprint

from django.utils.html import strip_tags
from rest_framework import serializers
from .models import Product, ProductOptions, Brand, Animal, Category


class ProductOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptions
        exclude = ('product', 'is_active', 'date_created', 'date_updated')


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionsSerializer(many=True, read_only=True)
    # min_price = serializers.Field(source='min_price_options')

    class Meta:
        model = Product
        fields = ('id', 'name', 'animal', 'brand', 'category', 'options', 'image',
                  'description', 'features', 'composition', 'additives', 'analysis')#, 'min_price')
        depth = 1

    # def get_min_price(self, obj):
    #     print(obj.id, 'eto ID')
    #     for _ in obj.options.all():
    #         print(f'{_.price}- eto price')
    #     print('-----------------------------------------------------------------------------------')
    #     # pprint(f'{obj.id}-eto ID, {obj.options.price}-eto price')
    #     return f'{obj.id} {obj.options.count()}'


    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['description'] = strip_tags(instance.description)
        data['features'] = strip_tags(instance.features)
        data['image'] = strip_tags(instance.image)
        data['composition'] = strip_tags(instance.composition)
        return data


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ('id', 'name', 'products',)
        # depth = 1


class AnimalSerializer(serializers.ModelSerializer):
    products = ProductSerializer

    class Meta:
        model = Animal
        fields = 'id', 'name', 'products'
        depth = 1


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        depth = 1

