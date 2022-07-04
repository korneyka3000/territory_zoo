from pprint import pprint

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from .models import Product, Brand, Animal, Category, ProductOptions
from rest_framework import viewsets
from .serializers import (ProductSerializer,
                          BrandSerializer,
                          AnimalSerializer,
                          CategorySerializer,
                          ProductOptionsSerializer, FilterProductSerializer, )


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

    @action(methods=['POST'], detail=False, filterset_fields=('brand', 'animal'))
    def filter_product(self, request):
        # pprint(request.__dict__)
        a = request.data
        # print(dir(request))
        print(a['filters'])
        # print(request.query_params)
        # print(self.kwargs)
        # print(self.filterset_fields)
        query_set = self.get_queryset().filter(**a['filters'])
        print(query_set)
        serializer = ProductSerializer(query_set, many=True)
        return Response(serializer.data)


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
