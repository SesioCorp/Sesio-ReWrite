# Generated by Django 3.2.16 on 2022-11-15 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0002_auto_20221103_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_type_text_number',
            field=models.TextField(blank=True, null=True),
        ),
    ]
