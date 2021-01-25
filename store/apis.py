from base_backend.permissions import IsAdminOrReadOnly, IsAdminOrIsOwner
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from store.filters import ProductFilter
from store.models import Category, SubCategory, Color, Product, OrderLine, Order, Favorite, Rate, Like, \
    ProductOnSeasonalDiscount, SeasonalDiscount, DeliveryFee
from store.serializers import CategorySerializer, SubCategorySerializer, ColorSerializer, ProductSerializer, \
    OrderLineSerializer, OrderSerializer, FavoriteSerializer, RateSerializer, LikeSerializer, \
    ProductOnSeasonalDiscountSerializer, SeasonalDiscountSerializer, DeliveryFeeSerializer


class DashboardStatistics(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        :param request:
        :param format:
        :return: Dashboard Statistics
        """
        data = {
            "total_orders": self.get_total_orders(),
            "pending_orders": self.get_pending_orders(),
            "canceled_orders": self.get_canceled_orders(),
            "confirmed_orders": self.get_confirmed_orders(),
            "delivered_orders": self.get_delivered_orders(),
            "on_delivery_orders": self.get_on_delivery_orders(),
        }

        return Response(data)

    def get_queryset(self):
        return Order.objects.filter(visible=True)

    def get_pending_orders(self):
        queryset = self.get_queryset()
        return queryset.filter(status='P').count()

    def get_canceled_orders(self):
        queryset = self.get_queryset()
        return queryset.filter(status="CA").count()

    def get_confirmed_orders(self):
        queryset = self.get_queryset()
        return queryset.filter(status='CO').count()

    def get_delivered_orders(self):
        queryset = self.get_queryset()
        return queryset.filter(status='D').count()

    def get_on_delivery_orders(self):
        queryset = self.get_queryset()
        return queryset.filter(status='OD').count()

    def get_total_orders(self):
        queryset = self.get_queryset()
        return queryset.count()


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
