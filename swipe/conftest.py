import pytest
from allauth.account.models import EmailAddress
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from user_app.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(email, password):
    user = User.objects.create_user(email=email, password=password, username=email, role='user')
    EmailAddress.objects.create(email=email, verified=True, primary=True, user_id=user.id)
    return user


@pytest.fixture()
def user_authenticate(api_client, create_user):
    user = create_user('test@example.com', 'password')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')
    return api_client
