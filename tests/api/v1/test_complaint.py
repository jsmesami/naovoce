import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from fruit.models import Fruit

REQUEST_DATA = {
    'text': 'complaint',
}


def test_complaint(client, random_password, new_user, new_fruit):
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-complaint', args=[fruit.id]), REQUEST_DATA)

    assert response.status_code == status.HTTP_201_CREATED
    assert REQUEST_DATA == response.json()


@pytest.mark.django_db
def test_complaint_nonexistent_fruit(client, truncate_table, random_password, new_user):
    truncate_table(Fruit)
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-complaint', args=[1]), REQUEST_DATA)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found.'}


def test_complaint_unauthorized(client, new_fruit):
    fruit = new_fruit()

    response = client.post(reverse('api:fruit-complaint', args=[fruit.id]), REQUEST_DATA)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_complaint_missing_text(client, random_password, new_user, new_fruit):
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-complaint', args=[fruit.id]), {'foo': 'bar'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'text': ['This field is required.']}
