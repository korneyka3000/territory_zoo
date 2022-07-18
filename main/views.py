from django.db.models import Prefetch, Count, Avg, Min, Q, Exists, Case, When, F
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Animal, Brand, Category, Product, ProductOptions, Article, Comments, InfoShop
from .serializers import (AnimalSerializer, BrandSerializer, CategorySerializer,
                          ProductSerializer, ProductOptionsSerializer, ArticleSerializer,  # CommentsSerializer,
                          InfoShopSerializer, CommentsSerializer, )
from collections import OrderedDict


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


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('animal', 'category',)
    search_fields = ('name',)
    ordering_fields = ('name', 'min_price', 'popular', 'minimal_price')
    ordering = ('name',)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        if len(response.data['results']) == 0:
            response.status_code = 400
        return response

    def get_queryset(self):
        queryset = Product.objects.all().annotate(minimal_price=Min('options__price', filter=Q(options__partial=False)))
        brands = self.request.query_params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand_id__in=brands)
        return queryset

    # def get_object(self):
    #     queryset = self.get_queryset().select_related()
    #     obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
    #     print(obj)
    #     return obj


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

    @action(detail=True, methods=['GET'], url_path='popular', name='popular_product_by_pet')
    def popular_by_pet(self, request, pk=None):
        instance = Product.objects.filter(animal=pk).order_by('-popular')
        if len(instance) < 16:
            serializer = ProductSerializer(instance, many=True)
        else:
            serializer = ProductSerializer(instance[:16], many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductOptionsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProductOptions.objects.filter(is_active=True)
    serializer_class = ProductOptionsSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Article.objects.filter(is_active=True)
    serializer_class = ArticleSerializer


class CommentsView(viewsets.ViewSet):

    def list(self, request):
        comments = Comments.objects.filter(published=True)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)


class InfoShopView(viewsets.ViewSet):

    queryset = InfoShop.objects.filter(published=True)
    serializer_class = InfoShopSerializer
