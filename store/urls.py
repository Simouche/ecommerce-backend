from django.urls import path
from rest_framework.routers import SimpleRouter

from store.apis import CategoryViewSet, SubCategoryViewSet, ColorViewSet, ProductViewSet, OrderViewSet, \
    OrderLineViewSet, FavoriteViewSet, RateViewSet, LikeViewSet, SeasonalDiscountViewSet, \
    ProductOnSeasonalDiscountViewSet, DeliveryFeeViewSet

router = SimpleRouter()

router.register('categories/sub-categories', SubCategoryViewSet, basename='sub-categories')
router.register('categories', CategoryViewSet, basename='categories')
router.register('colors', ColorViewSet, basename='colors')
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')
router.register('orders/lines', OrderLineViewSet, basename='order-lines')
router.register('favorite', FavoriteViewSet, basename='favorite')
router.register('rating', RateViewSet, basename='rating')
router.register('likes', LikeViewSet, basename='likes')
router.register('seasonal-discount', SeasonalDiscountViewSet, basename='seasonal-discount')
router.register('seasonal-discount/products', ProductOnSeasonalDiscountViewSet, basename='seasonal-discount-products')
router.register('delivery-fees', DeliveryFeeViewSet, basename='delivery-fees')

urlpatterns = [

              ] + router.urls
