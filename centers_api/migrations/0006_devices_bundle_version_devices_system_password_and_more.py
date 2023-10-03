# Generated by Django 4.1.4 on 2023-08-03 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centers_api', '0005_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='bundle_version',
            field=models.TextField(default='hello', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devices',
            name='system_password',
            field=models.TextField(default='Hello', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devices',
            name='windows_version',
            field=models.TextField(default='1.1.1.1', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='DeviceFiles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('type', models.CharField(choices=[('NA', 'NONE'), ('SV', 'SURVERY FORM'), ('TC', 'TOOLS CHARACTERISTICS'), ('SR', 'GIVEN SERVICES REPORT'), ('MC', 'MAINTENANCE CHECK LIST')], default='NA', max_length=2)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='centers_api.devices')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='centers_api.events')),
            ],
        ),
    ]