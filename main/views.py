from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product, Brand, Animal, Category, ProductOptions
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import ProductSerializer, BrandSerializer, AnimalSerializer, CategorySerializer, \
    ProductOptionsSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('brand', 'animal', 'category',)
    search_fields = ('name',)
    ordering_fields = ('name', 'brand', 'date_added',)
    ordering = ('name',)

    # def get_queryset  (self):
    #     query_set = Product.objects.all()
    #     brand = self.request.query_params.get('brand')
    #     print(len(brand))
    #     if brand:
    #         query_set = query_set.filter(brand_id=brand)
    #     return query_set


class BrandViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AnimalViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductOptionsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProductOptions.objects.all()
    serializer_class = ProductOptionsSerializer
