# Generated by Django 3.2.19 on 2023-06-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkerboard_app', '0004_rename_checherboard_checkerboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='number',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=3, verbose_name='Этаж номер'),
        ),
        migrations.AlterField(
            model_name='riser',
            name='number',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=3, verbose_name='Стояк номер'),
        ),
    ]
