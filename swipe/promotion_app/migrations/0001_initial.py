# Generated by Django 3.2.19 on 2023-06-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(choices=[('1', 'Подарок при покупке'), ('2', 'Возможет торг'), ('3', 'Квартира у моря'), ('4', 'В спальном районе'), ('5', 'Вам повезло с ценой'), ('6', 'Для большой семьй'), ('7', 'Семейное гнездышко'), ('8', 'Отдельная парковка')], default='', max_length=400, verbose_name='Добавить фразу')),
                ('highlight', models.CharField(max_length=10, verbose_name='Добавить цвет')),
                ('big', models.BooleanField(default=False, verbose_name='Большое')),
                ('raise_up', models.BooleanField(default=False, verbose_name='Поднять')),
                ('turbo', models.BooleanField(default=False, verbose_name='Турбо')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('payday', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Цена')),
                ('activ', models.BooleanField(default=False)),
            ],
        ),
    ]
