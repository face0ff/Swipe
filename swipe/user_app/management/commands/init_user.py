from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 1:
            email = 'owner@example.com'
            username = 'owner@example.com'
            password = 'owner'
            hashed_password = make_password(password)
            role = 'owner'
            user = User.objects.create_superuser(email=email, username=username, password=hashed_password, role=role)
            infrastructure = Infrastructure.objects.create(owner_id=user)
            infrastructure.save()
        else:
            print('Owner Готовченко')

        if User.objects.count() == 2:
            email = 'user@example.com'
            username = 'user@example.com'
            password = 'user'
            hashed_password = make_password(password)
            role = 'user'
            User.objects.create_superuser(email=email, username=username, password=hashed_password, role=role)
        else:
            print('User Готовченко')

        if User.objects.count() == 3:
            email = 'manager@example.com'
            username = 'manager@example.com'
            password = 'manager'
            hashed_password = make_password(password)
            role = 'manager'
            User.objects.create_superuser(email=email, username=username, password=hashed_password, role=role)
        else:
            print('Manager Готовченко')