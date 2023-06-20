import pytest
from rest_framework_simplejwt.tokens import AccessToken

from user_app.models import Notaries, Subscription, User
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestSubscription:
    endpoint = '/api/v1/subscription/'

    @pytest.fixture
    def create_one(self):
        one = Subscription.objects.create(
            paid_by="2023-06-20",
            auto_renewal=True
        )
        return one

    def test_get_subscription(self, user_authenticate):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_post_subscription(self, user_authenticate):
        value = {
            "paid_by": "2023-06-20",
            "auto_renewal": True
        }
        response = user_authenticate.post('/api/v1/subscription_create/', data=value)
        assert response.status_code == 201


    def test_put_subscription(self, create_one):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpassword', role='user')
        user.subscription = create_one
        user.save()
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')
        value = {
            "paid_by": "2023-06-20",
            "auto_renewal": False
        }
        response = api_client.put('/api/v1/subscription_update/', data=value)
        assert response.status_code == 200

