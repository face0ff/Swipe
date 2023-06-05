import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from user_app.models import User


@shared_task()
def test():
    today = datetime.date.today()
    target_date = today + datetime.timedelta(days=5)
    users_subscription = User.objects.filter(subscription__auto_renewal=False, subscription__paid_by__lte=target_date)
    for user in users_subscription:
        print(user.id, 'Ну подпишись уже, что тебе жалко')
# def send_email_task(email_list, msg):
#     for i in email_list:
#         send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, [i], html_message=msg)
