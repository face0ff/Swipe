import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user_app.models import User

pytestmark = pytest.mark.django_db


class TestUser:
    endpoint = '/api/auth/user/'

    def test_get_all_user_user(self, user_authenticate):
        response = user_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_all_user_manager(self, admin_authenticate):
        response = admin_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_get_all_user_owner(self, owner_authenticate):
        response = owner_authenticate.get(self.endpoint)
        assert response.status_code == 200

    def test_post_user(self):
        client = APIClient()
        value = {
            "email": "user1@example.com",
            "password1": "string",
            "password2": "string",
            "first_name": "string",
            "last_name": "string",
            "role": "user"
        }
        response = client.post('/api/v1/user_register/', data=value)
        assert response.status_code == 201

    def test_post_owner(self):
        client = APIClient()
        value = {
            "email": "user1@example.com",
            "password1": "string",
            "password2": "string",
            "first_name": "string",
            "last_name": "string",
            "role": "owner"
        }
        response = client.post('/api/v1/owner_register/', data=value)
        assert response.status_code == 201

    #
    def test_put_user(self):
        user = User.objects.create_user(email='user1@example.com', username='user1@example.com',
                                        password='testpassword',
                                        role='user')
        user.save()
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')
        file_path = "media/img/avatar/4.jpeg"  # Путь к файлу аватара
        file_name = os.path.basename(file_path)
        file_content = open(file_path, 'rb').read()
        avatar_file = SimpleUploadedFile(file_name, file_content, content_type='image/jpeg')

        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')

        value = {
            "avatar": avatar_file,
            "email": "user1@example.com",
            "password": "string",
            "last_name": "string",
            "first_name": "string",
            "telephone": "string",
            "notification": "me",
            "to_agent": True,
            "agent_first_name": "string",
            "agent_last_name": "string",
            "agent_telephone": "string",
            "agent_email": "user@example.com"
        }

        response = api_client.put('/api/v1/user_update/', data=value, format='multipart')
        assert response.status_code == 200

    def test_put_owner(self):
        user = User.objects.create_user(email='owner1@example.com', username='owner1@example.com',
                                        password='testpassword',
                                        role='owner')
        user.save()
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')
        value = {
            "email": "ownertest@example.com",
            "first_name": "string",
            "last_name": "string"
        }
        response = api_client.put('/api/v1/owner_update/', data=value, format='multipart')
        assert response.status_code == 200
