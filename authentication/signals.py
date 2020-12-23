from axes.signals import user_locked_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import PermissionDenied

from authentication.models import User, Profile


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, raw, **kwargs):
    if created and not raw:
        Profile.objects.create(user=instance)


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")
