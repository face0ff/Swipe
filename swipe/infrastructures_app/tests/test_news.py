import datetime

import pytest
from infrastructures_app.models import Corp, Section, News

pytestmark = pytest.mark.django_db


class TestNews:
    endpoint = '/api/v1/news/'

    @pytest.fixture
    def create_one(self, create_owner):
        one = News.objects.create(news_description='test', date=datetime.datetime.today(),
                                  infrastructure_id=create_owner.infrastructure)
        return one

    def test_get_news(self, user_authenticate, create_one):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_news_my_list(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}my_news/')
        assert response.status_code == 200

    def test_post_news(self, owner_authenticate, corp_create):
        value = {
            "news_description": "5"
        }
        response = owner_authenticate.post(self.endpoint, data=value)
        assert response.status_code == 201

    def test_retrieve_news(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 200

    def test_delete_news(self, owner_authenticate, create_one):
        response = owner_authenticate.delete(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 204
