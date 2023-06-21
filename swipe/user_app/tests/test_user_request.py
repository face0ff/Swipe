import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from infrastructures_app.models import Apartment
from user_app.models import User

pytestmark = pytest.mark.django_db


class TestUser:
    endpoint = '/api/v1/user_list/user_request/'



    def test_get_all_user_user(self, admin_authenticate):
        response = admin_authenticate.get(self.endpoint)
        assert response.status_code == 200

