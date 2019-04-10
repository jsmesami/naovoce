import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from . import TOKEN_BAD_ARGS
from ..utils import HTTP_METHODS
from user.models import FruitUser


def test_facebook_token(client, new_facebook_info, mock_facebook):
    fcb_info = new_facebook_info()
    existing_user = fcb_info.user
    request_data = {
        'email': existing_user.email,
        'fcb_id': fcb_info.fcb_id,
    }

    mock_facebook()

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    token = Token.objects.get(user=existing_user)

    expected = {
        'id': existing_user.id,
        'token': token.key,
    }

    assert response.json() == expected


@pytest.mark.django_db
def test_facebook_token_missing_user(client, truncate_table, random_email):
    truncate_table(FruitUser)
    request_data = {
        'email': random_email(),
        'fcb_id': 'some_id',
    }

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'non_field_errors': [
            'User with email {email} and Facebook ID {fcb_id} does not exist.'.format(**request_data)
        ]
    }


def test_facebook_token_wrong_fcb_id(client, new_facebook_info, new_user):
    fcb_info = new_facebook_info()
    request_data = {
        'email': fcb_info.user.email,
        'fcb_id': 'wrong_id',
    }

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'non_field_errors': [
            'User with email {email} and Facebook ID {fcb_id} does not exist.'.format(**request_data)
        ]
    }


@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('email', {'email': ['This field is required.']}),
        ('fcb_id', {'fcb_id': ['This field is required.']}),
    ]
)
def test_facebook_token_missing_args(client, new_facebook_info, missing_arg, error_msg):
    fcb_info = new_facebook_info()
    request_data = {
        'email': fcb_info.user.email,
        'fcb_id': fcb_info.fcb_id,
    }
    request_data.pop(missing_arg)

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize('bad_args, error_msg', TOKEN_BAD_ARGS)
def test_facebook_token_bad_args(client, signup_facebook_request_data, bad_args, error_msg):
    request_data = signup_facebook_request_data(**bad_args)

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_facebook_token_fcb_verification_failed(client, new_facebook_info, mock_facebook):
    fcb_info = new_facebook_info()
    request_data = {
        'email': fcb_info.user.email,
        'fcb_id': fcb_info.fcb_id,
    }

    mock_facebook(fails=True)

    response = client.post(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'non_field_errors': ['Facebook verification failed: Facebook error']}


@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'post', 'options'})
def test_facebook_token_bad_methods(client, new_facebook_info, mock_facebook, bad_method, bad_method_response):
    fcb_info = new_facebook_info()
    existing_user = fcb_info.user
    request_data = {
        'email': existing_user.email,
        'fcb_id': fcb_info.fcb_id,
    }

    mock_facebook()

    response = getattr(client, bad_method)(
        reverse('api:token-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
