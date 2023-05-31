import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Subscription(models.Model):
    paid_by = models.DateTimeField('Дата', auto_now=True)
    auto_renewal = models.BooleanField(default=True)


class User(AbstractUser):

    avatar = models.ImageField('Аватар', upload_to='img/avatar/')
    telephone = models.CharField('Телефон', max_length=20)
    agent_first_name = models.CharField('Имя', max_length=32)
    agent_last_name = models.CharField('Фамилия', max_length=32)
    agent_telephone = models.CharField('Телефон', max_length=20)
    agent_email = models.EmailField('Имейл', max_length=32)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE, null=True)
    NOTIF_CHOICES = (
        ('me', 'Мне'),
        ('me_and_agent', 'Мне и агенту'),
        ('agent', 'Агенту'),
        ('off', 'Отключить'),
    )
    notification = models.CharField(max_length=15, choices=NOTIF_CHOICES, default='me')
    to_agent = models.BooleanField(default=False)
    black_list = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('admin', 'Админ'),
        ('manager', 'Менеджер'),
        ('user', 'Юзер'),
        ('owner', 'Застроищик'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')
    favorite_infrastructures = models.ManyToManyField('infrastructures_app.Infrastructure', verbose_name='Пользователи', blank=True)
    favorite_apartments = models.ManyToManyField('infrastructures_app.Apartment', verbose_name='Пользователи', blank=True)


class UserRequest(models.Model):
    infrastructure_id = models.ForeignKey('infrastructures_app.Infrastructure', on_delete=models.CASCADE)
    apartment_id = models.ForeignKey('infrastructures_app.Apartment', on_delete=models.CASCADE)


class Message(models.Model):
    text = models.TextField('Текст сообщения')
    sender = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver',  on_delete=models.CASCADE)


class Notaries(models.Model):
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    telephone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Имейл', max_length=32)


