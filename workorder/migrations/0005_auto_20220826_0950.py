# Generated by Django 3.2.14 on 2022-08-26 14:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_auto_20220805_0821'),
        ('workorder', '0004_alter_workorder_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='asset',
            field=models.ManyToManyField(blank=True, null=True, related_name='work_orders', to='asset.Asset'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='enter_device_id_manually',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workorder',
            name='repair_images',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='scan_bar_code',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='workorder',
            name='status',
            field=models.CharField(blank=True, choices=[('open', 'Open'), ('closed', 'Closed')], max_length=50),
        ),
        migrations.AddField(
            model_name='workorder',
            name='work_orders_connected_to_an_asset',
            field=models.CharField(blank=True, choices=[('no', 'No'), ('yes', 'Yes')], max_length=50),
        ),
    ]