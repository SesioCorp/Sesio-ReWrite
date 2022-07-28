# Generated by Django 3.2.14 on 2022-07-27 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('short_description', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]