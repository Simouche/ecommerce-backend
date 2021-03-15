from django.db.models import Count, Sum
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from store.models import Order, Product


class DashboardStatistics(APIView):
    permission_classes = [IsAdminUser]

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
            "total_clients": self.get_total_clients(),
            "product_statistics": self.get_products_sales(),
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

    def get_total_clients(self):
        return User.objects.filter(user_type='C').count()

    def get_products_sales(self):
        data = Product.objects \
            .all() \
            .annotate(sales=Count("orders_lines"), sold_quantity=Sum("orders_lines__quantity")) \
            .values("id", "name", "price", "stock", "sales", "sold_quantity")
        return data


class CreateAdvertisementSms(CreateAPIView):
    serializer_class = None
    permission_classes = [IsAdminUser]


class CreateAdvertisementEmail(CreateAPIView):
    serializer_class = None
    permission_classes = [IsAdminUser]


class SendAdvertisementSms(APIView):
    pass


class SendAdvertisementEmail(APIView):
    pass
