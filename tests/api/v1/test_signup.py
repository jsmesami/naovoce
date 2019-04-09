import funcy
import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from .utils import HTTP_METHODS
from user import constants
from user.models import FruitUser

SIGNUP_BAD_ARGS = [
    ({'username': None},
     {'username': ['This field may not be null.']}),
    ({'username': ''},
     {'username': ['This field may not be blank.']}),
    ({'username': 'user\x00name'},
     {'username': ['Null characters are not allowed.']}),
    ({'username': 'u' * (constants.USERNAME_MAX_LENGTH + 1)},
     {'username': ['Ensure this field has no more than {} characters.'.format(constants.USERNAME_MAX_LENGTH)]}),
    ({'email': None},
     {'email': ['This field may not be null.']}),
    ({'email': ''},
     {'email': ['This field may not be blank.']}),
    ({'email': 'invalid'},
     {'email': ['Enter a valid email address.']}),
    ({'email': 'invalid@'},
     {'email': ['Enter a valid email address.']}),
    ({'email': 'invalid@domain'},
     {'email': ['Enter a valid email address.']}),
    ({'email': '@domain.com'},
     {'email': ['Enter a valid email address.']}),
    ({'password': None},
     {'password': ['This field may not be null.']}),
    ({'password': ''},
     {'password': ['This field may not be blank.']}),
    ({'password': 'abc'},
     {'password': ['Ensure this field has at least {} characters.'.format(settings.PASSWORD_MIN_LENGTH)]}),
]


@pytest.fixture
def signup_email_request_data(random_email, random_username, random_password):
    def closure(**kwargs):
        return {
            'email': kwargs.pop('email', random_email()),
            'username': kwargs.pop('username', random_username()),
            'password': kwargs.pop('password', random_password()),
        }

    return closure


@pytest.mark.django_db
def test_signup(client, signup_email_request_data):
    request_data = signup_email_request_data()

    response = client.post(
        reverse('api:signup'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_200_OK

    users = FruitUser.objects.prefetch_related('messages').filter(email=request_data['email'])

    assert users.count() == 1

    user = users[0]
    expected = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
    }

    assert user.is_email_verified is False
    assert user.messages.count() == 0
    assert request_data['email'] == expected['email']
    assert request_data['username'] == expected['username']
    assert response.json() == expected


@pytest.mark.django_db
@pytest.mark.parametrize('bad_args, error_msg', SIGNUP_BAD_ARGS)
def test_signup_bad_args(client, signup_email_request_data, bad_args, error_msg):
    response = client.post(
        reverse('api:signup'),
        signup_email_request_data(**bad_args),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.django_db
@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('email', {'email': ['This field is required.']}),
        ('username', {'username': ['This field is required.']}),
        ('password', {'password': ['This field is required.']}),
    ]
)
def test_signup_missing_args(client, signup_email_request_data, missing_arg, error_msg):
    response = client.post(
        reverse('api:signup'),
        funcy.omit(signup_email_request_data(), [missing_arg]),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.django_db
@pytest.mark.parametrize(
    'existing_field, error_msg', [
        ({'username': 'existing'}, {'username': ['User with this username already exists.']}),
        ({'email': 'existing@email.cz'}, {'email': ['User with this email already exists.']}),
    ]
)
def test_signup_user_exists(client, new_user, signup_email_request_data, existing_field, error_msg):
    new_user(username='existing', email='existing@email.cz')

    response = client.post(
        reverse('api:signup'),
        signup_email_request_data(**existing_field),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.django_db
@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'post', 'options'})
def test_signup_bad_methods(client, signup_email_request_data, bad_method, bad_method_response):
    request_data = signup_email_request_data()

    response = getattr(client, bad_method)(
        reverse('api:signup'),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
