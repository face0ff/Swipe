from django.core.management.base import BaseCommand

from user_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 0:
            email = 'admin@admin.com'
            username = 'admin@admin.com'
            password = 'admin'
            User.objects.create_superuser(email=email, username=username, password=password)
        else:
            print('Admin Готовченко')