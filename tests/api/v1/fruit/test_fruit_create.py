import funcy
import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from . import BAD_FRUIT_CRUD_ARGS


def test_fruit_create(client, random_password, new_user, fruit_request_data):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    request_data = fruit_request_data()
    response = client.post(
        reverse('api:fruit-list'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED

    created = response.json()

    assert user.username == created['user']['username']
    assert request_data == {
        'kind': created['kind'],
        'lat': created['lat'],
        'lng': created['lng'],
        'description': created['description'],
    }


def test_fruit_create_deleted_kind(client, random_password, new_user, fruit_request_data, deleted_kinds_keys):
    password = random_password()
    user = new_user(password=password)
    deleted_kind_key = deleted_kinds_keys()[0]

    assert client.login(username=user.username, password=password)

    request_data = fruit_request_data(kind=deleted_kind_key)

    response = client.post(
        reverse('api:fruit-list'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'kind': ['{key} is not a valid Kind key.'.format(key=deleted_kind_key)]}


@pytest.mark.parametrize('bad_args, error_msg', BAD_FRUIT_CRUD_ARGS)
def test_fruit_create_bad_args(client, random_password, new_user, fruit_request_data, bad_args, error_msg):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-list'),
        fruit_request_data(**bad_args),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('kind', {'kind': ['This field is required.']}),
        ('lat', {'lat': ['This field is required.']}),
        ('lng', {'lng': ['This field is required.']}),
    ]
)
def test_fruit_create_missing_args(client, random_password, new_user, fruit_request_data, missing_arg, error_msg):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-list'),
        funcy.omit(fruit_request_data(), [missing_arg]),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.django_db
def test_fruit_create_unauthenticated(client, fruit_request_data):
    response = client.post(
        reverse('api:fruit-list'),
        fruit_request_data(),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_fruit_create_unauthorized(client, random_password, new_user, fruit_request_data):
    password = random_password()
    user = new_user(password=password, is_email_verified=False)

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-list'),
        fruit_request_data(),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}
