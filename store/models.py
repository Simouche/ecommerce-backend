import decimal
import os
import uuid

from base_backend.models import DeletableModel, _, do_nothing
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.db import models
# Create your models here.
from django.db.models import Avg, Sum, F

from ecommerce.settings import MEDIA_ROOT, MEDIA_URL, HOST_NAME
from store.managers import CustomCategoryManager


class Category(DeletableModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    objects = CustomCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class SubCategory(DeletableModel):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    category = models.ForeignKey('Category', related_name='sub_categories', verbose_name=_('Category'),
                                 on_delete=do_nothing)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'category'),)
        verbose_name = _('Sub-Category')
        verbose_name_plural = _('Sub-Categories')


class Color(models.Model):
    name = models.CharField(max_length=20)
    hex = models.CharField(max_length=9)

    def __str__(self):
        return "{} {}".format(self.name, self.hex)


class Product(DeletableModel):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(verbose_name=_('Price'), max_digits=10, decimal_places=2)
    main_image = models.ImageField(verbose_name=_('Main Image'), upload_to='products')  # ToDo add save to
    slider = ArrayField(models.CharField(max_length=255, ), null=True, blank=True)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Discount Price'), null=True,
                                         blank=True)
    colors = models.ManyToManyField('Color', related_name='products', blank=True)
    dimensions = models.CharField(max_length=30, verbose_name=_('Dimensions'), null=True, blank=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ForeignKey('SubCategory', on_delete=do_nothing, related_name='products',
                                 verbose_name=_('Category'), null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def slider_urls(self):
        images = []
        paths = os.listdir(self.slider)
        for path in paths:
            images.append(HOST_NAME + self.slider + path)
        return images

    @property
    def overall(self):
        return self.ratings.filter(visible=True).aggregate(overall=Avg('stars')).get('overall', 0) or 0

    @property
    def total_reviews_count(self):
        return self.ratings.filter(visible=True).count()

    @property
    def reviews_count_based_on_stars(self):
        return [self.ratings.filter(visible=True, stars__lte=1).count(),
                self.ratings.filter(visible=True, stars__in=[1, 2.1]).count(),
                self.ratings.filter(visible=True, stars__in=[2.1, 3.1]).count(),
                self.ratings.filter(visible=True, stars__in=[3.1, 4]).count(),
                self.ratings.filter(visible=True, stars__in=[4.1, 5.1]).count()]

    @staticmethod
    def make_product_slider_directory():
        path = os.path.join(MEDIA_ROOT, "products/sliders", uuid.uuid4().__str__())
        os.makedirs(path, exist_ok=True)
        return path + "/"

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-id']


class ColorImages(DeletableModel):
    product = models.ForeignKey('Product', on_delete=do_nothing, related_name="color_images")
    color = models.ForeignKey('Color', on_delete=do_nothing, related_name="products_images")
    image = models.ImageField(upload_to="products")

    class Meta:
        verbose_name = _('Colored Images')
        verbose_name_plural = _('Colored Images')


class OrderLine(DeletableModel):
    product = models.ForeignKey('Product', related_name='orders_lines', on_delete=do_nothing)
    order = models.ForeignKey('Order', related_name='lines', on_delete=do_nothing)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    on_discount = models.BooleanField(default=False, verbose_name=_('On Discount'))

    def __str__(self):
        return '{} {}'.format(self.quantity, self.product)

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')


class Order(DeletableModel):
    status_choices = (('P', _('Pending')),
                      ('CO', _('Confirmed')),
                      ('CA', _('Canceled')),
                      ('OD', _('On Delivery')),
                      ('D', _('Delivered')))

    profile = models.ForeignKey('authentication.Profile', related_name='orders', on_delete=do_nothing)
    number = models.CharField(max_length=16, unique=True, verbose_name=_('Order Number'))
    status = models.CharField(max_length=2, choices=status_choices, verbose_name=_('Order Status'), default='P')

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.profile.user

    @property
    def products_count(self):
        return self.get_lines.aggregate(count=Sum('quantity')).get('count', 0)

    @property
    def total_sum(self):
        total = 0
        for line in self.get_lines:
            total += line.total
        return total.quantize(decimal.Decimal("0.01"))

    @property
    def get_lines(self):
        return self.lines.filter(visible=True)

    @staticmethod
    def generate_number():
        from random import randint
        return randint(11111, 99999)

    def __str__(self):
        return '{}'.format(self.number)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def progress_status(self):
        if self.status == 'P':
            self.status = 'CO'
        elif self.status == 'CO':
            self.status = 'OD'
        elif self.status == 'OD':
            self.status = 'D'
        else:
            self.status = 'CO'
        self.save()

    def delete(self, using=None, keep_parents=False):
        if self.status == 'D':
            return
        self.status = 'CA'
        super(Order, self).delete(using=using, keep_parents=keep_parents)


class Favorite(DeletableModel):
    profile = models.ForeignKey('authentication.Profile', related_name='favorites', on_delete=do_nothing)
    product = models.ForeignKey('Product', related_name='favorites', on_delete=do_nothing)

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.profile.owner

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')


class Rate(DeletableModel):
    stars = models.DecimalField(max_digits=1, decimal_places=1, verbose_name=_('Stars'))
    comment = models.CharField(max_length=255, null=True, verbose_name=_('Comment'))
    profile = models.ForeignKey('authentication.Profile', related_name='ratings', on_delete=do_nothing)
    product = models.ForeignKey('Product', related_name='ratings', on_delete=do_nothing)

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.profile.user

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')

    @property
    def checked_stars_range(self):
        return range(0, int(self.stars))

    @property
    def un_checked_stars_range(self):
        return range(0, 5 - int(self.stars))


class Like(DeletableModel):
    profile = models.ForeignKey('authentication.Profile', related_name='likes', on_delete=do_nothing)
    product = models.ForeignKey('Product', related_name='likes', on_delete=do_nothing)

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.profile.user

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class CartLine(DeletableModel):
    product = models.ForeignKey('Product', related_name='cart_lines', on_delete=do_nothing)
    cart = models.ForeignKey('Cart', related_name='lines', on_delete=do_nothing)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.cart.get_owner

    def _total_sum(self):
        return self.product.price * self.quantity

    @property
    def total_sum(self):
        return self._total_sum().quantize(decimal.Decimal("0.01"))

    class Meta:
        verbose_name = _('Cart Line')
        verbose_name_plural = _('Cart Lines')


class Cart(DeletableModel):
    profile = models.OneToOneField('authentication.Profile', related_name='cart', on_delete=do_nothing)

    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.profile.user

    @property
    def products_count(self):
        return 0

    @property
    def total_sum(self):
        return self.lines.aggregate(total=Sum(F('quantity') * F('product__price'))).get('total', 0) \
            .quantize(decimal.Decimal('0.01'))

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class SeasonalDiscount(DeletableModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    period = DateRangeField(verbose_name=_('Period'))
    global_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name=_('Discount'))
    products = models.ManyToManyField('Product', through='ProductOnSeasonalDiscount')

    class Meta:
        verbose_name = _('Seasonal Discount')
        verbose_name_plural = _('Seasonal Discounts')


class ProductOnSeasonalDiscount(DeletableModel):
    product = models.ForeignKey('Product', related_name='seasonal_discounts', on_delete=do_nothing)
    seasonal_discount = models.ForeignKey('SeasonalDiscount', on_delete=do_nothing)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name=_('Discount'))

    class Meta:
        verbose_name = _('Product On Seasonal Discount')
        verbose_name_plural = _('Products On Seasonal Discount')


class DeliveryFee(DeletableModel):
    region = models.ForeignKey('authentication.Region', related_name='fees', on_delete=do_nothing)
    fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _('Delivery Fee')
        verbose_name_plural = _('Delivery Fees')
