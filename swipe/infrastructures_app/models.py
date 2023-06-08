import datetime

from django.db import models

from checkerboard_app.models import Riser, Floor
from promotion_app.models import Promotion
from user_app.models import User


# from swipe.promotion_app.models import Promotion


# Create your models here.

class Infrastructure(models.Model):
    address = models.CharField('Адрес', max_length=64, null=True)
    STATUS_CHOICE = (
        ('apart', 'Квартира'),
        ('house', 'Дом')
    )
    status = models.CharField('Статус', choices=STATUS_CHOICE, max_length=20, default='apart')
    VIEW_CHOICE = (
        ('multifamily', 'многоквартирный'),
        ('singlefamily', 'одноквартирный')
    )
    view = models.CharField('Тип', choices=VIEW_CHOICE, max_length=20, default='singlefamily')
    TECHNOLOGY_CHOICE = (
        ('panel', 'Панельный'),
        ('monolith', 'Монолит')
    )
    technology = models.CharField('Технология', choices=TECHNOLOGY_CHOICE, max_length=20, default='panel')
    TERRITORY_CHOICE = (
        ('close', 'Закрытая'),
        ('open', 'Открытая')
    )
    territory = models.CharField('Территория', choices=TERRITORY_CHOICE, max_length=20, default='close')
    distance = models.DecimalField('Дистанция', max_digits=10, decimal_places=0, null=True)
    celling_height = models.DecimalField('Высота потолков', max_digits=1, decimal_places=0, null=True)
    ELECTRICITY_CHOICE = (
        ('yes', 'Подключено'),
        ('not', 'Отключено')
    )
    electricity = models.CharField('Электричество', choices=ELECTRICITY_CHOICE, max_length=20, default='yes')
    GAS_CHOICE = (
        ('yes', 'Есть'),
        ('not', 'Нет')
    )
    gas = models.CharField('Газ', choices=GAS_CHOICE, max_length=20, default='yes')
    HEATING_CHOICE = (
        ('central', 'Центрайльное'),
        ('individual', 'Индивидуальное')
    )
    heating = models.CharField('Отопление', choices=HEATING_CHOICE, max_length=20, default='central')
    SEWAGE_CHOICE = (
        ('central', 'Центрайльное'),
        ('individual', 'Индивидуальное')
    )
    sewage = models.CharField('Каннализация', choices=SEWAGE_CHOICE, max_length=20, default='central')
    WATTER_CHOICE = (
        ('central', 'Центрайльное'),
        ('individual', 'Индивидуальное')
    )
    watter_supply = models.CharField('Водоснабжение', choices=WATTER_CHOICE, max_length=20, default='central')
    map = models.TextField('Карта', null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Apartment(models.Model):
    VIEW_CHOICE = (
        ('secondary', 'Вторичное жилье'),
        ('primary', 'Новострой'),
        ('cottage', 'Коттедж')
    )
    view = models.CharField('Вид', choices=VIEW_CHOICE, max_length=20, default='primary')
    TECHNOLOGY_CHOICE = (
        ('panel', 'Панельный'),
        ('monolith', 'Монолит')
    )
    technology = models.CharField('Технология', choices=TECHNOLOGY_CHOICE, max_length=20, default='panel')
    STATUS_CHOICE = (
        ('rented', 'Сдан'),
        ('vacant', 'Не сдан')
    )
    status = models.CharField('Статус', choices=STATUS_CHOICE, max_length=20, default='rented')
    QUANTITY_CHOICE = (
        ('1', '1-комнатная'),
        ('2', '2-комнатная'),
        ('3', '3-комнатная'),
        ('4', '4-комнатная')
    )
    quantity = models.CharField('Количество комнат', choices=QUANTITY_CHOICE, max_length=20, default='1')
    APPOINTMENT_CHOICE = (
        ('Residential', 'Жилая'),
        ('Commercial', 'Коммерческая'),
        ('Industrial', 'Промышленная')
    )
    appointment = models.CharField('Вид', choices=APPOINTMENT_CHOICE, max_length=20, default='Residential')
    STATE_CHOICE = (
        ('need', 'Требует ремонта'),
        ('building', 'Ремонт от строителей')
    )
    state = models.CharField('Жилое состояние', choices=STATE_CHOICE, max_length=20, default='building')
    PLANE_CHOICE = (
        ('studio', 'Студия'),
        ('standart', 'Стандарт'),
        ('open', 'Свободная'),
        ('penthouse', 'Пентхаус')
    )
    plane = models.CharField('Планировка', choices=PLANE_CHOICE, max_length=20, default='open')
    area = models.DecimalField('Площадь', decimal_places=1, max_digits=3)
    kitchen_area = models.DecimalField('Площадь кухни', decimal_places=1, max_digits=3)
    BALCONY_CHOICE = (
        ('yes', 'Да'),
        ('not', 'Нет')
    )
    balcony = models.CharField('Планировка', choices=BALCONY_CHOICE, max_length=20, default='yes')
    HEATING_CHOICE = (
        ('electro', 'Электрическое'),
        ('gas', 'Газовое')
    )
    heating = models.CharField('Газ', choices=HEATING_CHOICE, max_length=20, default='yes')
    PAY_CHOICE = (
        ('cash', 'Наличные'),
        ('maternity', 'Мат. капитал'),
        ('mortgage', 'Ипотека'),
        ('military', 'Военная ипотека'),
        ('not', 'Неважно')
    )
    payment = models.CharField('Варианты расчета', choices=PAY_CHOICE, max_length=20, blank=True)
    commission = models.DecimalField('Коммисия агенту', decimal_places=1, max_digits=10)
    COMMUNICATION_CHOICE = (
        ('call', 'Звонок'),
        ('message', 'Сообщение'),
        ('two', 'Звонок+Сообщение')
    )
    communication = models.CharField('Способ связи', choices=COMMUNICATION_CHOICE, max_length=20, default='call')
    apart_description = models.TextField('Описание', max_length=400)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)
    infrastructure_id = models.ForeignKey('Infrastructure', on_delete=models.CASCADE)
    riser_id = models.ForeignKey(Riser, on_delete=models.CASCADE)
    floors_id = models.ForeignKey(Floor, on_delete=models.CASCADE)
    schema = models.ImageField('Схема', upload_to='img/schema/')
    REJECTION_CHOICE = (
        ('ok', 'Все ок'),
        ('foto', 'Фото'),
        ('price', 'Цена'),
        ('description', 'Описание'),
    )
    rejection = models.CharField('Причины отклонения', choices=REJECTION_CHOICE, max_length=20, blank=True)


class Image(models.Model):
    image = models.ImageField('', upload_to='img/image/')
    infrastructure_id = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)


class ImageApart(models.Model):
    image = models.ImageField('', upload_to='img/image/')
    apartment_id = models.ForeignKey(Apartment, on_delete=models.CASCADE)


class Docs(models.Model):
    file = models.FileField('Документы', upload_to='file/docs/')
    is_excel = models.BooleanField('Ексель', default=False)
    infrastructure_id = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)


class News(models.Model):
    date = models.DateTimeField('Дата', auto_now_add=True)
    news_description = models.TextField('', max_length=600)
    infrastructure_id = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)


class Corp(models.Model):
    number = models.DecimalField('Корпус номер', max_digits=3, decimal_places=0)
    infrastructure_id = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)


class Section(models.Model):
    number = models.DecimalField('Секция номер', max_digits=3, decimal_places=0)
    corp_id = models.ForeignKey(Corp, on_delete=models.CASCADE)
