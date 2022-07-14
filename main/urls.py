from django.urls import path
from rest_framework.routers import DefaultRouter
from main.views import ProductViewSet, BrandViewSet, AnimalViewSet, CategoryViewSet, ProductOptionsViewSet
from main.views_excel import import_csv, export_csv

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'animals', AnimalViewSet, basename='animals')
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register('import/', import_csv, basename="Import_csv")
# router.register('export/', export_csv, basename="export_users_csv")


urlpatterns = router.urls

urlpatterns = [

    path('import/', import_csv, name="Import_csv"),
    path('export/', export_csv, name="export_users_csv"),

]