# Generated by Django 3.2.14 on 2022-09-05 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0008_auto_20220905_1337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='assigned',
            new_name='assigned_to',
        ),
    ]
