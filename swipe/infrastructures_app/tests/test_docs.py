import datetime
import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from infrastructures_app.models import Corp, Section, News, Docs

pytestmark = pytest.mark.django_db


class TestDocs:
    endpoint = '/api/v1/docs/'

    @pytest.fixture
    def create_one(self, create_owner):
        file_path = "media/file/docs/example_7.xlsx"  # Путь к файлу аватара
        file_name = os.path.basename(file_path)
        file_content = open(file_path, 'rb').read()
        file = SimpleUploadedFile(file_name, file_content, content_type='image/jpeg')
        one = Docs.objects.create(is_excel=True, file=file,
                                  infrastructure_id=create_owner.infrastructure)
        return one

    def test_get_docs(self, user_authenticate, create_one):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_docs_my_list(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}my_docs/')
        assert response.status_code == 200

    def test_post_docs(self, owner_authenticate, corp_create):
        file_path = "media/file/docs/example_7.xlsx"  # Путь к файлу аватара
        file_name = os.path.basename(file_path)
        file_content = open(file_path, 'rb').read()
        file = SimpleUploadedFile(file_name, file_content, content_type='image/jpeg')
        value = {
            "file": file,
            'is_excel': True
        }
        response = owner_authenticate.post(self.endpoint, data=value)
        assert response.status_code == 201

    def test_retrieve_docs(self, owner_authenticate, create_one):
        response = owner_authenticate.get(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 200

    def test_delete_docs(self, owner_authenticate, create_one):
        response = owner_authenticate.delete(f'{self.endpoint}{create_one.id}/')
        assert response.status_code == 204
