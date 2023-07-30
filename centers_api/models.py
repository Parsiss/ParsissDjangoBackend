from django.db import models

# Create your models here.
class Centers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, null=False, blank=False)



class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.TextField(max_length=100)
    center = models.ForeignKey(Centers, on_delete=models.CASCADE, related_name='devices')

