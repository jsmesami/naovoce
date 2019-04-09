import facebook
import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from .utils import HTTP_METHODS
from user import constants
from user.models import FruitUser, FacebookInfo

FCB_ID = '110045436843169'

FCB_TOKEN = (
    'EAADvcY7nZCq8BAGbU0JMgZCaOPtQZBZBuioYJcIghkoFu2A26HWWzykYhcnVYY6ihNZBVh'
    'QlHFpnMeZBAhpobEA6bGTLbPw3Fqbfsv8SfgsP2augzlcWFcZCe2uDDs9DP6f3PNZBZAM0c'
    'OnwxdhzRorxugOfO1EHJuyw2jhcQMZCzJVCfhq8FWpb40CmFPwg1WNQbtktW11hOiggZDZD'
)

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


@pytest.fixture
def signup_facebook_request_data(random_email):
    def closure(**kwargs):
        return {
            'email': kwargs.pop('email', random_email()),
            'fcb_id': kwargs.pop('fcb_id', FCB_ID),
            'fcb_token': kwargs.pop('fcb_token', FCB_ID),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_facebook_info(new_user):
    def closure(**kwargs):
        return FacebookInfo.objects.create(
            user=kwargs.pop('user', None) or new_user(),
            fcb_id=kwargs.pop('fcb_id', FCB_ID),
            fcb_token=kwargs.pop('fcb_token', FCB_TOKEN),
            **kwargs
        )

    return closure


@pytest.fixture
def mock_facebook(monkeypatch):
    def closure(fails=False, **overrides):
        def get_object(*args, **kwargs):
            if fails:
                raise facebook.GraphAPIError('Facebook error')

            return {
                'first_name': overrides.pop('first_name', 'Isaac'),
                'last_name': overrides.pop('last_name', 'Asimov'),
                'id': overrides.pop('fcb_id', FCB_ID),
                'picture': {
                    'data': {
                        'height': 200,
                        'is_silhouette': True,
                        'url': 'https://platform-lookaside.fbsbx.com/platform/profilepic/'
                               '?asid=110045436843169&height=200&width=200&ext=1556829832&hash=AeSLD93lbSjc5t96',
                        'width': 200,
                    },
                },
            }

        monkeypatch.setattr(facebook.GraphAPI, 'get_object', get_object)

    return closure


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


@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'post', 'options'})
@pytest.mark.django_db
def test_facebook_signup_bad_methods(
    client, signup_facebook_request_data, mock_facebook, bad_method, bad_method_response
):
    request_data = signup_facebook_request_data()

    mock_facebook()

    response = getattr(client, bad_method)(
        reverse('api:signup-fcb'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)


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
