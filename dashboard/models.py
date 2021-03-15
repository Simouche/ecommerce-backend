from base_backend.models import DeletableModel, _
from django.db import models


# Create your models here.


class BaseAdvertisement(DeletableModel):
    receivers = models.ManyToManyField('authentication.User', related_name="received_emails",
                                       verbose_name=_('Receivers'))
    content = models.TextField(verbose_name=_('Content'))
    send_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class AdvertisementEmail(BaseAdvertisement):
    subject = models.CharField(max_length=255, verbose_name=_('Subject'), null=True)


class AdvertisementSms(BaseAdvertisement):
    pass
