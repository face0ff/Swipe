from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 0:
            email = 'admin@example.com'
            username = 'admin@example.com'
            password = 'admin'
            hashed_password = make_password(password)
            role = 'admin'
            User.objects.create_superuser(email=email, username=username, password=hashed_password, role=role)
        else:
            print('Admin Готовченко')