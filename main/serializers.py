from rest_framework import serializers
from .models import Product, ProductOptions, Brand, Animal, Category


class ProductOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptions
        exclude = ('product',)


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'
        depth = 1


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = '__all__'
        depth = 1


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        depth = 1
