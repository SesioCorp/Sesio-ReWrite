# Generated by Django 3.2.14 on 2022-08-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pirority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
