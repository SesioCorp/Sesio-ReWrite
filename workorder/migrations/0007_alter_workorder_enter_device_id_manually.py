# Generated by Django 3.2.14 on 2022-09-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0006_auto_20220830_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='enter_device_id_manually',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
