import datetime

from django.db import models

# Create your models here.


class Promotion(models.Model):
    PHRASE_CHOICES = (
        ('1', 'Подарок при покупке'),
        ('2', 'Возможет торг'),
        ('3', 'Квартира у моря'),
        ('4', 'В спальном районе'),
        ('5', 'Вам повезло с ценой'),
        ('6', 'Для большой семьй'),
        ('7', 'Семейное гнездышко'),
        ('8', 'Отдельная парковка'),
    )
    phrase = models.CharField('Добавить фразу', max_length=400, choices=PHRASE_CHOICES, default='')
    highlight = models.CharField('Добавить цвет', max_length=10)
    big = models.BooleanField('Большое', default=False)
    raise_up = models.BooleanField('Поднять', default=False)
    turbo = models.BooleanField('Турбо', default=False)
    date = models.DateField('Дата', auto_now=True)
    payday = models.DecimalField('Цена', max_digits=3, decimal_places=2)
    activ = models.BooleanField(default=False)

