import json

import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from user import constants

TOKEN_BAD_ARGS = [
    ({'username': 'u' * (constants.USERNAME_MAX_LENGTH + 1)},
     {'non_field_errors': ['Unable to log in with provided credentials.']}),
    ({'username': None},
     {'username': ['This field may not be null.']}),
    ({'username': ''},
     {'username': ['This field may not be blank.']}),
    ({'password': 'bad_password'},
     {'non_field_errors': ['Unable to log in with provided credentials.']}),
    ({'password': 'p' * (constants.PASSWORD_MAX_LENGTH + 1)},
     {'non_field_errors': ['Unable to log in with provided credentials.']}),
    ({'password': None},
     {'password': ['This field may not be null.']}),
    ({'password': ''},
     {'password': ['This field may not be blank.']}),
]


def test_obtain_token(client, random_password, new_user):
    password = random_password()
    user = new_user(password=password)
    request_data = {
        'username': user.username,
        'password': password,
    }

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    token = Token.objects.get(user=user)

    expected = {
        'id': user.id,
        'token': token.key,
    }

    assert response.json() == expected


@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('username', {'username': ['This field is required.']}),
        ('password', {'password': ['This field is required.']}),
    ]
)
def test_obtain_token_missing_args(client, random_password, new_user, missing_arg, error_msg):
    password = random_password()
    user = new_user(password=password)
    request_data = {
        'username': user.username,
        'password': password,
    }
    request_data.pop(missing_arg)

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize('bad_args, error_msg', TOKEN_BAD_ARGS)
def test_obtain_token_bad_args(client, random_password, new_user, bad_args, error_msg):
    password = random_password()
    user = new_user(password=password)
    request_data = {
        'username': user.username,
        'password': password,
        **bad_args
    }

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_obtain_token_unverified_user(client, random_password, new_user):
    password = random_password()
    user = new_user(password=password, is_email_verified=False)
    request_data = {
        'username': user.username,
        'password': password,
    }

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': "User's email is not verified."}


def test_obtain_token_user_not_active(client, random_password, new_user):
    password = random_password()
    user = new_user(password=password, is_active=False)
    request_data = {
        'username': user.username,
        'password': password,
    }

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'non_field_errors': ['Unable to log in with provided credentials.']}


def test_token_can_authenticate(random_password, new_user, new_fruit):
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()
    request_data = {
        'username': user.username,
        'password': password,
    }
    client = APIClient()

    response = client.post(
        reverse('api:token'),
        json.dumps(request_data),
        content_type='application/json',
    )

    request_data = {
        'text': 'complaint'
    }
    client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        json.dumps(request_data),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == request_data
