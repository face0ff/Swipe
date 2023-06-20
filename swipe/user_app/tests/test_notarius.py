import pytest

from user_app.models import Notaries

pytestmark = pytest.mark.django_db


class TestNotaries:
    endpoint = '/api/v1/notaries/'

    @pytest.fixture
    def create_one(self):
        one = Notaries.objects.create(first_name='Notaries 1')
        return one

    def test_get_notarius(self, user_authenticate):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_post_notaries(self, admin_authenticate):
        value = {
            "first_name": "string",
            "last_name": "string",
            "telephone": "string",
            "email": "user@example.com"
        }
        response = admin_authenticate.post(self.endpoint, data=value)
        assert response.status_code == 201

    def test_retrieve_notaries(self, user_authenticate, create_one):
        response = user_authenticate.get(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 200

    def test_put_notaries(self, admin_authenticate, create_one):
        value = {
            "first_name": "1231",
            "last_name": "string",
            "telephone": "string",
            "email": "user@example.com"
        }
        response = admin_authenticate.put(f'{self.endpoint}{create_one.id}/', data=value)
        assert response.status_code == 200

    def test_delete_notaries(self, admin_authenticate, create_one):
        response = admin_authenticate.delete(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 204