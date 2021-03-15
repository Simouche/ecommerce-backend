from django_filters import rest_framework as filters

from store.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_discount_price = filters.NumberFilter(field_name="discount_price", lookup_expr='gte')
    max_discount_price = filters.NumberFilter(field_name="discount_price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'category__name', 'category__category', 'category__category__name', 'price',
                  'min_price', 'max_price', 'min_discount_price', 'max_discount_price', 'colors__id', 'colors__name',
                  'colors__hex', 'name']
