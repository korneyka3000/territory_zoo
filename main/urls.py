from main.views import ProductViewSet, BrandViewSet, AnimalViewSet, CategoryViewSet, ProductOptionsViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'animals', AnimalViewSet, basename='animals')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'options', ProductOptionsViewSet, basename='options')



urlpatterns = [
    # path('products', )
]
urlpatterns += router.urls
