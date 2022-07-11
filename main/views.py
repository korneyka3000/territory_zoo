from collections import OrderedDict
from django.db.models import Prefetch, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
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
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        self.get_count_qs = queryset.count()
        return super(Pagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page_number', self.page.number),
            ('products_on_page', self.page.end_index() - self.page.start_index() + 1),
            ('total_products', self.get_count_qs),
            ('total_pages', self.page.paginator.num_pages),
            ('max_products_on_page', self.get_page_size(self.request)),
            ('results', data),
        ]))

# class MyOrderFilter(OrderingFilter):
#     def filter_queryset(self, request, queryset, view):
#         ordering = self.get_ordering(request, queryset, view)
#
#         if ordering:
#             print(ordering)
#             if 'options__price' in ordering:
#                 return queryset.order_by(*ordering)
#             return queryset.order_by(*ordering)
#         return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all().prefetch_related(
        Prefetch('options', queryset=ProductOptions.objects.all())
    )
    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('animal', 'category',)
    search_fields = ('name',)
    ordering_fields = ('name', 'options__price',)
    ordering = ('name',)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        if len(response.data['results']) == 0:
            response.status_code = 400
        return response

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

    # lookup_field = ('name',)
    # def get_object(self):
    #     qs = self.get_queryset()#.prefetch_related('products')
    #     print(qs)
    #     print(self.kwargs)
    #     obj = get_object_or_404(qs, **self.kwargs)
    #     print(obj)
    #     return obj



class AnimalViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductOptionsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProductOptions.objects.all().order_by('price')
    serializer_class = ProductOptionsSerializer
