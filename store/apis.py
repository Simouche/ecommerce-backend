from base_backend.permissions import IsAdminOrReadOnly, IsAdminOrIsOwner
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from store.filters import ProductFilter
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
    queryset = Color.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    model = Product

    @action(methods=['post'], detail=False, url_path='multiple', permission_classes=[IsAdminUser])
    def delete_many(self, request, *args, **kwargs):
        products_ids = request.data.get('ids')
        products = self.get_queryset().filter(pk__in=products_ids)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderLineViewSet(ModelViewSet):
    serializer_class = OrderLineSerializer
    queryset = OrderLine.objects.filter(visible=True)
    permission_classes = [IsAdminOrIsOwner]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.filter(visible=True)
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrIsOwner]

    def get_queryset(self):
        queryset = super(OrderViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(profile__user=self.request.user)


class FavoriteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.filter(visible=True)

    def get_queryset(self):
        queryset = super(FavoriteViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(profile__user=self.request.user)


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
