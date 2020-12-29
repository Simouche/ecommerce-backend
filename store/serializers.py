from rest_framework.fields import ReadOnlyField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from store.models import Category, SubCategory, Color, Product, OrderLine, Order, Favorite, Rate, Like, \
    SeasonalDiscount, ProductOnSeasonalDiscount, DeliveryFee


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_categories']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class ProductSerializer(ModelSerializer):
    category = StringRelatedField()
    colors = ColorSerializer(many=True, required=False)
    overall = ReadOnlyField()
    total_reviews_count = ReadOnlyField()
    reviews_count_based_on_stars = ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'main_image', 'slider', 'discount_price', 'colors',
                  'dimensions', 'stock', 'category', 'overall', 'total_reviews_count', 'reviews_count_based_on_stars']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'colors': {
                'required': False
            }
        }



class OrderLineSerializer(ModelSerializer):
    total = ReadOnlyField(source='total')

    class Meta:
        model = OrderLine
        fields = ['id', 'product', 'order', 'quantity', 'on_discount', 'total']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
        }


class OrderSerializer(ModelSerializer):
    sum = ReadOnlyField(source='total_sum')
    count = ReadOnlyField(source='products_count')
    lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'profile', 'number', 'status', 'count', 'sum', 'lines']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'profile': {
                'read_only': True,
            },
            'number': {
                'read_only': True,
            },
            'status': {
                'read_only': True,
            },
        }


class FavoriteSerializer(ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Favorite
        fields = ['id', 'profile', 'product']


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'stars', 'comment', 'profile', 'product']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'profile', 'product']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class ProductOnSeasonalDiscountSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductOnSeasonalDiscount
        fields = ['id', 'product', 'seasonal_discount', 'discount']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class SeasonalDiscountSerializer(ModelSerializer):
    products = ProductOnSeasonalDiscountSerializer()

    class Meta:
        model = SeasonalDiscount
        fields = ['id', 'name', 'period', 'global_discount', 'products']
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class DeliveryFeeSerializer(ModelSerializer):
    region = StringRelatedField()

    class Meta:
        model = DeliveryFee
        fields = ['id', 'fee', 'region']
