import datetime

import pytest
from infrastructures_app.models import Corp, Section, News

pytestmark = pytest.mark.django_db


class TestNews:
    endpoint = '/api/v1/infrastructure/'

    def test_get_infrastructure(self, user_authenticate):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_infrastructure_my_list(self, owner_authenticate):
        response = owner_authenticate.get(f'{self.endpoint}my_infrastructure/')
        assert response.status_code == 200

    # def test_put_infrastructure(self, owner_authenticate, create_owner):
    #     value = {
    #
    #         "images": [
    #             {
    #                 "image": "string",
    #                 "image_place": 1,
    #                 "image_delete": True
    #             }
    #         ],
    #         "photo": "string",
    #         "address": "string",
    #         "status": "apart",
    #         "view": "multifamily",
    #         "technology": "panel",
    #         "territory": "close",
    #         "distance": "1",
    #         "celling_height": "1",
    #         "electricity": "yes",
    #         "gas": "yes",
    #         "heating": "central",
    #         "sewage": "central",
    #         "watter_supply": "central",
    #         "map": "string"
    #     }
    #
    #     response = owner_authenticate.put(f'{self.endpoint}{create_owner.infrastructure.id}/', data=value)
    #     assert response.status_code == 200

    def test_retrieve_infrastructure(self, owner_authenticate, create_owner):
        response = owner_authenticate.get(f'{self.endpoint}{create_owner.infrastructure.id}/')
        assert response.status_code == 200

    def test_delete_news(self, owner_authenticate, create_owner):
        response = owner_authenticate.delete(f'{self.endpoint}{create_owner.infrastructure.id}/')
        assert response.status_code == 204
