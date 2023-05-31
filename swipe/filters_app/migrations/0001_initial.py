# Generated by Django 4.2.1 on 2023-05-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.CharField(choices=[('secondary', 'Вторичное жилье'), ('primary', 'Новострой'), ('cottage', 'Коттедж'), ('all', 'Все')], default='all', verbose_name='Вид')),
                ('status', models.CharField(choices=[('rented', 'Сдан'), ('vacant', 'Не сдан')], default='rented', verbose_name='Статус')),
                ('district', models.CharField(max_length=100, verbose_name='Район')),
                ('microdistrict', models.CharField(max_length=100, verbose_name='Микрорайон')),
                ('quantity', models.CharField(choices=[('1', '1-комнатная'), ('2', '2-комнатная'), ('3', '3-комнатная'), ('4', '4-комнатная')], default='1', verbose_name='Количество комнат')),
                ('price_from', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена от')),
                ('price_to', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена до')),
                ('area_from', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Площадь от')),
                ('area_to', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Площадь до')),
                ('purpose', models.CharField(choices=[('apart', 'Квартира'), ('house', 'Дом')], default='apart', verbose_name='Статус')),
                ('payment', models.CharField(blank=True, choices=[('cash', 'Наличные'), ('maternity', 'Мат. капитал'), ('mortgage', 'Ипотека'), ('military', 'Военная ипотека'), ('not', 'Неважно')], verbose_name='Варианты расчета')),
                ('state', models.CharField(choices=[('need', 'Требует ремонта'), ('building', 'Ремонт от строителей')], default='building', verbose_name='Жилое состояние')),
            ],
        ),
    ]