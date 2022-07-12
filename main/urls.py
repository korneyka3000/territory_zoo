from rest_framework.routers import DefaultRouter
from main.views import ProductViewSet, BrandViewSet, AnimalViewSet, CategoryViewSet, ProductOptionsViewSet


router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'animals', AnimalViewSet, basename='animals')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
