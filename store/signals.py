from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from store.models import OrderLine

order_line_deleted = Signal()


@receiver(post_save, sender=OrderLine)
def order_line_created(sender, instance: OrderLine, created, raw, **kwargs):
    if created:
        instance.product.stock = F('stock') - instance.quantity


@receiver(order_line_deleted)
def order_line_deleted(sender, instance: OrderLine):
    instance.product.stock = F('stock') + instance.quantity
