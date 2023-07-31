from django.db import models
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Centers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, null=False, blank=False)


class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.TextField(max_length=100)
    center = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name='devices')


class Events(models.Model):
    class EventType(models.TextChoices):
        NONE = 'NA', _('NONE')
        SERVICE = 'SV', _('SERVICE')

    type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.NONE,
    )

    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField()
    description = models.TextField()
