# Generated by Django 3.2.14 on 2022-08-01 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_pirority'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pirority',
            new_name='Priority',
        ),
    ]
