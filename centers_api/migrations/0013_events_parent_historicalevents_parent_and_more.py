# Generated by Django 4.1.4 on 2023-12-22 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centers_api', '0012_devicehints_is_essential_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='centers_api.events'),
        ),
        migrations.AddField(
            model_name='historicalevents',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='centers_api.events'),
        ),
        migrations.AlterField(
            model_name='events',
            name='type',
            field=models.CharField(choices=[('NA', 'NONE'), ('SV', 'SERVICE'), ('FC', 'FACTOR')], default='NA', max_length=2),
        ),
        migrations.AlterField(
            model_name='historicalevents',
            name='type',
            field=models.CharField(choices=[('NA', 'NONE'), ('SV', 'SERVICE'), ('FC', 'FACTOR')], default='NA', max_length=2),
        ),
    ]
