# Generated by Django 4.1.4 on 2023-07-30 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centers_api', '0002_alter_centers_id_alter_devices_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Centers',
            new_name='Center',
        ),
        migrations.RenameModel(
            old_name='Devices',
            new_name='Device',
        ),
    ]