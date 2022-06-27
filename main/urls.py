#
# from django.urls import path, include
#
# from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
# from rest_framework_swagger.views import get_swagger_view

from main.views import ProductViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
# schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# urlpatterns = [
#     path('', schema_view, name='docs'),
#     path('products/', include(router.urls))
# ]
urlpatterns = router.urls
