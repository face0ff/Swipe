# Generated by Django 3.2.19 on 2023-06-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion_app', '0005_promotion_activ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='payday',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='Цена'),
        ),
    ]
