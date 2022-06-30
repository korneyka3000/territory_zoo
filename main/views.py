# from rest_framework.authtoken.admin import User
# from rest_framework.permissions import AllowAny
# from rest_framework.schemas import SchemaGenerator
# from rest_framework.views import APIView
# from rest_framework_swagger import renderers

from .models import Product, Brand, Animal, Category
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductSerializer, BrandSerializer, AnimalSerializer, CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AnimalViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


