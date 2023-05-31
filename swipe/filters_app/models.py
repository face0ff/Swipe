from django.db import models

from user_app.models import User


# Create your models here.


class Filter(models.Model):
    VIEW_CHOICE = (
        ('secondary', 'Вторичное жилье'),
        ('primary', 'Новострой'),
        ('cottage', 'Коттедж'),
        ('all', 'Все')
    )
    view = models.CharField('Вид', choices=VIEW_CHOICE, max_length=20, default='all')
    STATUS_CHOICE = (
        ('rented', 'Сдан'),
        ('vacant', 'Не сдан')
    )
    status = models.CharField('Статус', choices=STATUS_CHOICE, max_length=20, default='rented')
    district = models.CharField('Район', max_length=100)
    microdistrict = models.CharField('Микрорайон', max_length=100)
    QUANTITY_CHOICE = (
        ('1', '1-комнатная'),
        ('2', '2-комнатная'),
        ('3', '3-комнатная'),
        ('4', '4-комнатная')
    )
    quantity = models.CharField('Количество комнат', choices=QUANTITY_CHOICE, max_length=20, default='1')
    price_from = models.DecimalField('Цена от', max_digits=10, decimal_places=2)
    price_to = models.DecimalField('Цена до', max_digits=10, decimal_places=2)
    area_from = models.DecimalField('Площадь от', max_digits=10, decimal_places=2)
    area_to = models.DecimalField('Площадь до', max_digits=10, decimal_places=2)
    PURPOSE_CHOICE = (
        ('apart', 'Квартира'),
        ('house', 'Дом')
    )
    purpose = models.CharField('Статус', choices=PURPOSE_CHOICE, max_length=20, default='apart')
    PAY_CHOICE = (
        ('cash', 'Наличные'),
        ('maternity', 'Мат. капитал'),
        ('mortgage', 'Ипотека'),
        ('military', 'Военная ипотека'),
        ('not', 'Неважно')
    )
    payment = models.CharField('Варианты расчета', choices=PAY_CHOICE, max_length=20, blank=True)
    STATE_CHOICE = (
        ('need', 'Требует ремонта'),
        ('building', 'Ремонт от строителей')
    )
    state = models.CharField('Жилое состояние', choices=STATE_CHOICE, max_length=20, default='building')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
