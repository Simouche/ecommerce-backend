from base_backend.permissions import IsAdminOrReadOnly, IsAdminOrIsOwner
from django_filters import rest_framework as filters
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
    queryset = Color.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(visible=True)
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', 'category__category', 'colors', 'colors', 'discount_price', 'price', 'name')

    def apply_filters(self, queryset):
        m_queryset = queryset
        filters = self.request.query_params
        if filters.get("category", None):
            m_queryset = m_queryset.filter(category__category_id=filters.get("category"))
        if filters.get("sub_category", None):
            m_queryset = m_queryset.filter(category_id=filters.get("sub_category"))
        if filters.getlist("colors", None):
            m_queryset = m_queryset.filter(colors__id__in=filters.getlist("colors", None))
        if filters.get("in_stock", None):
            m_queryset = m_queryset.filter(stock__gt=0)
        if filters.get("on_discount", None):
            m_queryset = m_queryset.filter(discount_price__gt=0)
        if filters.get("price_min", None):
            m_queryset = m_queryset.filter(price__gte=filters.get("price_min"))
        if filters.get("price_max", None):
            m_queryset = m_queryset.filter(price__lte=filters.get("price_max"))
        if filters.get("name", None):
            m_queryset = m_queryset.filter(name__icontains=filters.get("name"))

        return m_queryset

    # def get_queryset(self):
    #     queryset = super(ProductViewSet, self).get_queryset()
    #     if self.action == 'list':
    #         queryset = self.apply_filters(queryset)
    #         return queryset
    #     return queryset


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
