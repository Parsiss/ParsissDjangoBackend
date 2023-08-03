from django.db import models
from django.utils.translation import gettext_lazy as _


import os 


# Create your models here.
class Centers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, null=False, blank=False)



class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.TextField(max_length=100)
    bundle_version = models.TextField(max_length=100)
    windows_version = models.TextField(max_length=100)
    system_password = models.TextField(max_length=100)
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



class DeviceFiles(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    device = models.ForeignKey(to=Devices, related_name='files', on_delete=models.CASCADE)
    event = models.ForeignKey(to=Events, related_name='files', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)

    def filename(self):
        return os.path.basename(self.file.name)
    

    class DeviceFileType(models.TextChoices):
        NONE = 'NA', _('NONE')
        SURVERY = 'SV', _('SURVERY FORM')
        TOOLS = 'TC', _('TOOLS CHARACTERISTICS')
        SERVICES = 'SR', _('GIVEN SERVICES REPORT')
        MAINTENANCE = 'MC', _('MAINTENANCE CHECK LIST')
    
    type = models.CharField(
        max_length=2,
        choices=DeviceFileType.choices,
        default=DeviceFileType.NONE,
    )

