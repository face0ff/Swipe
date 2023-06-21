import pytest
from infrastructures_app.models import Corp, Section

pytestmark = pytest.mark.django_db


class TestSection:
    endpoint = '/api/v1/section/'

    @pytest.fixture
    def create_one(self, corp_create):
        one = Section.objects.create(number=1, corp_id=corp_create)
        return one

    def test_get_section(self, user_authenticate, create_one):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_section_my_list(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}list')
        assert response.status_code == 200

    def test_post_section(self, owner_authenticate, corp_create):
        value = {
            "number": "5",
            'corp_id': corp_create.id
        }
        response = owner_authenticate.post(self.endpoint, data=value)
        assert response.status_code == 201

    def test_retrieve_section(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 200

    def test_delete_section(self, owner_authenticate, create_one):
        response = owner_authenticate.delete(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 204
