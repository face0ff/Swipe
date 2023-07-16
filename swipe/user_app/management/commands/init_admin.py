from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand

from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 0:
            email = 'admin@example.com'
            username = 'admin@example.com'
            password = 'admin'
            role = 'admin'
            user = User.objects.create_superuser(email=email, username=username, password=password, role=role)
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            print('go')
        else:
            print('Admin Готовченко')