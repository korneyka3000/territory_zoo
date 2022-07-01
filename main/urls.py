from main.views import ProductViewSet, BrandViewSet, AnimalViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'animals', AnimalViewSet, basename='animals')
router.register(r'categories', CategoryViewSet, basename='categories')



urlpatterns = [
    # path('api/products')
]
urlpatterns += router.urls
