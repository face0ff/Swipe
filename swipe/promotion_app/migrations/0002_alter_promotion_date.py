# Generated by Django 3.2.19 on 2023-05-27 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
    ]
