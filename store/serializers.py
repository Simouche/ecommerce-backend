from base_backend.utils import handle_uploaded_file
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
    category_name = StringRelatedField(source="category")
    colors = ColorSerializer(many=True, required=False)
    overall = ReadOnlyField()
    total_reviews_count = ReadOnlyField()
    reviews_count_based_on_stars = ReadOnlyField()
    slider_urls = ReadOnlyField()

    def create(self, validated_data):
        slider = validated_data.pop("slider") if validated_data.get('slider') else []
        path = Product.make_product_slider_directory()
        for image in slider:
            handle_uploaded_file(image, path + image.name)
        validated_data.update({'slider': path})
        product = Product.objects.create(**validated_data)
        return product

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'main_image', 'slider', 'discount_price', 'colors',
                  'dimensions', 'stock', 'category', 'category_name', 'overall', 'total_reviews_count',
                  'reviews_count_based_on_stars', 'slider_urls']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'category': {
                'write_only': True,
            },
            'colors': {
                'required': False
            }
        }


class OrderLineSerializer(ModelSerializer):
    total = ReadOnlyField()

    class Meta:
        model = OrderLine
        fields = ['id', 'product', 'order', 'quantity', 'on_discount', 'total']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'order': {
                'required': False
            },
        }


class OrderSerializer(ModelSerializer):
    sum = ReadOnlyField(source='total_sum')
    count = ReadOnlyField(source='products_count')
    lines = OrderLineSerializer(many=True)

    def create(self, validated_data):
        lines = validated_data.pop('lines')
        number = Order.generate_number()
        order = Order.objects.create(number=number, profile=self.context['request'].user.profile, **validated_data)
        for line in lines:
            OrderLine.objects.create(order=order, **line)
        return order

    def update(self, instance, validated_data):
        if validated_data.get('lines'):
            lines = validated_data.pop('lines')
            for line in lines:
                OrderLine.objects.create(order=instance, **line)
            return instance
        else:
            super(OrderSerializer, self).update(instance, validated_data)

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
                'required': False,
            }
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
