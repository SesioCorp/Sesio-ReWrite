# Generated by Django 3.2.14 on 2022-08-30 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0005_auto_20220826_0950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='brief_discription',
            new_name='brief_description',
        ),
        migrations.RenameField(
            model_name='workorder',
            old_name='discription',
            new_name='description',
        ),
    ]
