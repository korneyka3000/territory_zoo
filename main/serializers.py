from django.utils.html import strip_tags
from rest_framework import serializers
from .models import (Animal, Article, Brand, Category, Comments, InfoShop,
                     Product, ProductOptions, ProductImage, Order, Customer, OrderItem, Units, )


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        exclude = ('id',)


class ProductOptionsSerializer(serializers.ModelSerializer):
    units = UnitsSerializer(read_only=True)

    class Meta:
        model = ProductOptions
        exclude = ('product', 'is_active', 'date_created', 'date_updated',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('product',)


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionsSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    chosen_option = serializers.IntegerField(default=None)

    class Meta:
        model = Product
        fields = ('id', 'name', 'animal', 'brand', 'category', 'options', 'chosen_option', 'images',
                  'description', 'features', 'composition', 'additives', 'analysis',)
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['description'] = strip_tags(instance.description)
        data['features'] = strip_tags(instance.features)
        data['composition'] = strip_tags(instance.composition)
        data['additives'] = strip_tags(instance.additives)
        data['analysis'] = strip_tags(instance.analysis)
        return data


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'name', 'image')


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = ('id', 'name', 'image',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 1


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = ('date_added', 'published')


class InfoShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoShop
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('phone_number', 'customer_name',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True, many=False)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('customer', 'paid', 'items',)
