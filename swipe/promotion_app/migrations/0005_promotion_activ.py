# Generated by Django 3.2.19 on 2023-06-06 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion_app', '0004_auto_20230606_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='activ',
            field=models.BooleanField(default=False),
        ),
    ]
