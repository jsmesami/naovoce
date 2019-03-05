import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from user import constants
from user.models import FruitUser

TOKEN_BAD_ARGS = [
    ({'email': 'e' * (constants.EMAIL_MAX_LENGTH + 1)},
     {'email': [
         'Ensure this field has no more than {} characters.'.format(constants.EMAIL_MAX_LENGTH),
         'Enter a valid email address.',
     ]}),
    ({'email': None},
     {'email': ['This field may not be null.']}),
    ({'email': ''},
     {'email': ['This field may not be blank.']}),
    ({'fcb_id': 'i' * (constants.FCB_ID_MAX_LENGTH + 1)},
     {'fcb_id': ['Ensure this field has no more than {} characters.'.format(constants.FCB_ID_MAX_LENGTH)]}),
    ({'fcb_id': None},
     {'fcb_id': ['This field may not be null.']}),
    ({'fcb_id': ''},
     {'fcb_id': ['This field may not be blank.']}),
]
SIGNUP_BAD_ARGS = TOKEN_BAD_ARGS + [
    ({'fcb_token': 't' * (constants.FCB_TOKEN_MAX_LENGTH + 1)},
     {'fcb_token': ['Ensure this field has no more than {} characters.'.format(constants.FCB_TOKEN_MAX_LENGTH)]}),
    ({'fcb_token': None},
     {'fcb_token': ['This field may not be null.']}),
    ({'fcb_token': ''},
     {'fcb_token': ['This field may not be blank.']}),
]


@pytest.mark.django_db
def test_facebook_signup(client, truncate_table, signup_facebook_request_data, mock_facebook):
    truncate_table(FruitUser)
    request_data = signup_facebook_request_data()

    mock_facebook()

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    user = FruitUser.objects.get(email=request_data['email'])
    token = Token.objects.get(user=user)

    expected = {
        'id': user.id,
        'token': token.key,
    }

    assert response.json() == expected
    assert user.facebook.fcb_id == request_data['fcb_id']
    assert user.facebook.fcb_token == request_data['fcb_token']


@pytest.mark.django_db
def test_facebook_signup_user_exists(client, truncate_table, new_user, signup_facebook_request_data, mock_facebook):
    truncate_table(FruitUser)
    existing_user = new_user(is_email_verified=False)
    request_data = signup_facebook_request_data(email=existing_user.email)

    mock_facebook()

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    existing_user = FruitUser.objects.get(email=request_data['email'])
    token = Token.objects.get(user=existing_user)

    expected = {
        'id': existing_user.id,
        'token': token.key,
    }

    assert response.json() == expected
    assert existing_user.facebook.fcb_id == request_data['fcb_id']
    assert existing_user.facebook.fcb_token == request_data['fcb_token']
    assert existing_user.is_email_verified is True


def test_facebook_signup_fcb_info_exists(client, new_facebook_info, signup_facebook_request_data, mock_facebook):
    fcb_info = new_facebook_info()
    request_data = signup_facebook_request_data(
        email=fcb_info.user.email,
        fcb_id=fcb_info.fcb_id, fcb_token='new_token'
    )

    mock_facebook()

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    user = FruitUser.objects.get(email=request_data['email'])
    token = Token.objects.get(user=user)

    expected = {
        'id': user.id,
        'token': token.key,
    }

    assert response.json() == expected
    assert user.facebook.fcb_id == request_data['fcb_id']
    assert user.facebook.fcb_token == request_data['fcb_token']


@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('email', {'email': ['This field is required.']}),
        ('fcb_id', {'fcb_id': ['This field is required.']}),
        ('fcb_token', {'fcb_token': ['This field is required.']}),
    ]
)
def test_facebook_signup_missing_args(client, signup_facebook_request_data, missing_arg, error_msg):
    request_data = signup_facebook_request_data()
    request_data.pop(missing_arg)

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize('bad_args, error_msg', SIGNUP_BAD_ARGS)
def test_facebook_signup_bad_args(client, signup_facebook_request_data, bad_args, error_msg):
    request_data = signup_facebook_request_data(**bad_args)

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_facebook_signup_fcb_verification_failed(client, signup_facebook_request_data, mock_facebook):
    request_data = signup_facebook_request_data()

    mock_facebook(fails=True)

    response = client.post(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'non_field_errors': ['Facebook verification failed: Facebook error']}


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
