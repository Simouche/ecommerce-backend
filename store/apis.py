from base_backend.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from store.models import Category, SubCategory, Color, Product, OrderLine, Order, Favorite, Rate, Like, \
    ProductOnSeasonalDiscount, SeasonalDiscount, DeliveryFee
from store.serializers import CategorySerializer, SubCategorySerializer, ColorSerializer, ProductSerializer, \
    OrderLineSerializer, OrderSerializer, FavoriteSerializer, RateSerializer, LikeSerializer, \
    ProductOnSeasonalDiscountSerializer, SeasonalDiscountSerializer, DeliveryFeeSerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]


class ColorViewSet(ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]


class OrderLineViewSet(ModelViewSet):
    serializer_class = OrderLineSerializer
    queryset = OrderLine.objects.filter(visible=True)
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.filter(visible=True)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class FavoriteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.filter(visible=True)


class RateViewSet(ModelViewSet):
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Rate.objects.filter(visible=True)


class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.filter(visible=True)


class ProductOnSeasonalDiscountViewSet(ModelViewSet):
    serializer_class = ProductOnSeasonalDiscountSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ProductOnSeasonalDiscount.objects.filter(visible=True)


class SeasonalDiscountViewSet(ModelViewSet):
    serializer_class = SeasonalDiscountSerializer
    queryset = SeasonalDiscount.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]


class DeliveryFeeViewSet(ModelViewSet):
    serializer_class = DeliveryFeeSerializer
    queryset = DeliveryFee.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]
