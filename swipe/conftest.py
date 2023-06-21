import pytest
from allauth.account.models import EmailAddress
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

import user_app.serializers
from infrastructures_app.models import Infrastructure, Corp
from user_app.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        admin = User.objects.create_superuser(email='admin@example.com', username='admin@example.com',
                                              password='string', role='manager')
        EmailAddress.objects.create(email=admin.email, verified=True, primary=True, user_id=admin.id)
        user = User.objects.create_user(email='user@example.com', username='user@example.com', password='string',
                                        role='user')
        EmailAddress.objects.create(email=user.email, verified=True, primary=True, user_id=user.id)

        owner = User.objects.create_user(email='owner@example.com', username='owner@example.com', password='string',
                                         role='owner')
        infrastructure = Infrastructure.objects.create(owner=owner)
        EmailAddress.objects.create(email=owner.email, verified=True, primary=True, user_id=owner.id)


@pytest.fixture
def create_user():
    return User.objects.get(role='user')


@pytest.fixture()
def user_authenticate(api_client, create_user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(create_user)}')
    return api_client


@pytest.fixture
def create_admin():
    return User.objects.get(role='manager')


@pytest.fixture()
def admin_authenticate(api_client, create_admin):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(create_admin)}')
    return api_client


@pytest.fixture
def create_owner():
    return User.objects.get(role='owner')


@pytest.fixture()
def owner_authenticate(api_client, create_owner):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(create_owner)}')
    return api_client



@pytest.fixture()
def infrastructure_create(create_owner):
    infrastructure = Infrastructure.objects.create(owner=create_owner)
    return infrastructure

@pytest.fixture()
def corp_create(create_owner):
    corp = Corp.objects.create(number=1, infrastructure_id=create_owner.infrastructure)
    return corp
