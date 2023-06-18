import pytest

from user_app.models import Notaries


@pytest.mark.django_db
def test_notarius(user_authenticate):
    print('11111111111111111')
    Notaries.objects.create(first_name='Notarius 1')
    Notaries.objects.create(first_name='Notarius 2')
    response = user_authenticate.get('notaries')
    assert response.status_code == 200