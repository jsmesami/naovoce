import json

import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from . import TOKEN_BAD_ARGS
from ..utils import HTTP_METHODS


def test_obtain_token(client, random_password, new_user, user_auth):
    password = random_password()
    user = new_user(password=password)
    request_data = user_auth(password=password, user=user)

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
def test_obtain_token_missing_args(client, user_auth, missing_arg, error_msg):
    request_data = user_auth()
    request_data.pop(missing_arg)

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize('bad_args, error_msg', TOKEN_BAD_ARGS)
def test_obtain_token_bad_args(client, user_auth, bad_args, error_msg):
    request_data = {
        **user_auth(),
        **bad_args
    }

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_obtain_token_unverified_user(client, random_password, new_user, user_auth):
    password = random_password()
    user = new_user(password=password, is_email_verified=False)
    request_data = user_auth(password=password, user=user)

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': "User's email is not verified."}


def test_obtain_token_user_not_active(client, random_password, new_user, user_auth):
    password = random_password()
    user = new_user(password=password, is_active=False)
    request_data = user_auth(password=password, user=user)

    response = client.post(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'non_field_errors': ['Unable to log in with provided credentials.']}


def test_token_can_authenticate(user_auth, new_fruit):
    fruit = new_fruit()
    request_data = user_auth()
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


@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'post', 'options'})
def test_obtain_token_bad_methods(client, user_auth, bad_method, bad_method_response):
    request_data = user_auth()

    response = getattr(client, bad_method)(
        reverse('api:token'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
