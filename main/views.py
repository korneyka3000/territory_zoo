from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product, Brand, Animal, Category, ProductOptions
from rest_framework import viewsets
from .serializers import (ProductSerializer,
                          BrandSerializer,
                          AnimalSerializer,
                          CategorySerializer,
                          ProductOptionsSerializer,)


class Pagination(PageNumberPagination):
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        self.get_count_qs = queryset.count()
        return super(Pagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        print(type(data))
        return Response(OrderedDict([
            ('total_product', self.get_count_qs),
            ('max_products_on_page', self.get_page_size(self.request)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ]))


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('animal', 'category',)
    search_fields = ('name',)
    ordering_fields = ('name', 'options__price', 'date_added',)
    ordering = ('name',)

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, args, kwargs)
    #     if len(response.data) == 0:
    #         response.status_code = 403
    #     print(response.status_code)
    #     print(response.data)
    #     # response.data['one_more'] = 5
    #     return response

    # def filter_queryset(self, queryset):
    #     for backend in list(self.filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, self)
    #         print(queryset)
    #     return queryset

    def get_queryset(self):
        queryset = Product.objects.all()
        brands = self.request.query_params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand_id__in=brands)
        return queryset


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
