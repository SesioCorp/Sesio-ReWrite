# Generated by Django 3.2.14 on 2022-09-09 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_auto_20220805_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='barcode',
        ),
        migrations.AddField(
            model_name='asset',
            name='device_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]