from django.urls import path
from rest_framework.routers import DefaultRouter
from main.views import ProductViewSet, BrandViewSet, AnimalViewSet, CategoryViewSet, ProductOptionsViewSet, \
    ArticleViewSet, CommentsView, InfoShopView

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'animals', AnimalViewSet, basename='animals')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'comments', CommentsView, basename='comments')
# router.register(r'shop-info', InfoShopView.as_view(), basename='shop_info')
urlpatterns = [
    # path('comments/', CommentsView.as_view()),#, name='comments'),
    # path('shop-info/', InfoShopView.as_view()),#, name='shop_info'),
]
urlpatterns += router.urls
