import pytest
from infrastructures_app.models import Corp

pytestmark = pytest.mark.django_db


class TestCorp:
    endpoint = '/api/v1/corp/'

    @pytest.fixture
    def create_one(self, create_owner):
        one = Corp.objects.create(number=1, infrastructure_id=create_owner.infrastructure)
        return one

    def test_get_corp(self, user_authenticate, create_one):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_corp_my_list(self, owner_authenticate, create_one):
        response = owner_authenticate.get('/api/v1/corp/list')
        assert response.status_code == 200

    def test_post_corp(self, owner_authenticate, create_one):
        value = {
            "number": "5",
        }
        response = owner_authenticate.post('/api/v1/corp/create', data=value)
        assert response.status_code == 201

    def test_retrieve_corp(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 200

    def test_delete_corp(self, owner_authenticate, create_one):
        response = owner_authenticate.delete(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 204
