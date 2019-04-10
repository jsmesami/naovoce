import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from . import REQUEST_DATA, BAD_COMPLAINT_CREATE_ARGS
from ..utils import HTTP_METHODS
from fruit.models import Fruit, Comment


def test_complaint(client, truncate_table, random_password, new_user, new_fruit, user_auth):
    truncate_table(Comment)
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(**user_auth(user=user, password=password))

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert REQUEST_DATA == response.json()

    comment = Comment.objects.last()

    assert comment.fruit_id == fruit.id
    assert comment.author_id == user.id
    assert comment.text == REQUEST_DATA['text']
    assert comment.is_complaint is True


@pytest.mark.django_db
def test_complaint_nonexistent_fruit(client, truncate_table, user_auth):
    truncate_table(Fruit)

    assert client.login(**user_auth())

    response = client.post(
        reverse('api:fruit-complaint', args=[1]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found.'}


def test_complaint_unauthorized(client, new_fruit):
    fruit = new_fruit()

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


@pytest.mark.parametrize('bad_args, error_msg', BAD_COMPLAINT_CREATE_ARGS)
def test_complaint_bad_args(client, user_auth, new_fruit, bad_args, error_msg):
    fruit = new_fruit()

    assert client.login(**user_auth())

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        bad_args,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'post', 'options'})
def test_complaint_bad_methods(client, new_fruit, user_auth, bad_method, bad_method_response):
    fruit = new_fruit()

    assert client.login(**user_auth())

    response = getattr(client, bad_method)(
        reverse('api:fruit-complaint', args=[fruit.id]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
