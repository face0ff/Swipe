from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from infrastructures_app.models import Infrastructure
from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 1:
            email = 'owner@example.com'
            username = 'owner@example.com'
            password = 'owner'
            role = 'owner'
            user = User.objects.create_superuser(email=email, username=username, password=password, role=role)
            infrastructure = Infrastructure.objects.create(owner_id=user)
            infrastructure.save()
            user.save()
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            print('go')
        else:
            print('Owner Готовченко')

        if User.objects.count() == 2:
            email = 'user@example.com'
            username = 'user@example.com'
            password = 'user'
            role = 'user'
            user = User.objects.create_superuser(email=email, username=username, password=password, role=role)
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            print('go')
        else:
            print('User Готовченко')

        if User.objects.count() == 3:
            email = 'manager@example.com'
            username = 'manager@example.com'
            password = 'manager'
            role = 'manager'
            user = User.objects.create_superuser(email=email, username=username, password=password, role=role)
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            print('go')
        else:
            print('Manager Готовченко')