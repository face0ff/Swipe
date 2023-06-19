# Generated by Django 3.2.19 on 2023-06-13 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkerboard_app', '0005_auto_20230613_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='number',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name='Этаж номер'),
        ),
        migrations.AlterField(
            model_name='riser',
            name='number',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name='Стояк номер'),
        ),
    ]
