# from rest_framework.authtoken.admin import User
# from rest_framework.permissions import AllowAny
# from rest_framework.schemas import SchemaGenerator
# from rest_framework.views import APIView
# from rest_framework_swagger import renderers

from .models import Product
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(user)
        return Response(serializer.data)




