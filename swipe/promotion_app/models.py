import datetime

from django.db import models

# Create your models here.


class Promotion(models.Model):

    phrase = models.CharField('Добавить фразу', max_length=400)
    highlight = models.CharField('Добавить цвет', max_length=10)
    big = models.BooleanField('Большое', default=False)
    raise_up = models.BooleanField('Поднять', default=False)
    turbo = models.BooleanField('Турбо', default=False)
    date = models.DateTimeField('Дата', auto_now=True)
    payday = models.DecimalField('Цена', max_digits=3, decimal_places=2)

