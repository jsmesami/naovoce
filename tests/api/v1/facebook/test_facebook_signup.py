import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from user.models import FruitUser

from ..utils import HTTP_METHODS
from . import SIGNUP_BAD_ARGS


@pytest.mark.django_db
def test_facebook_signup(client, truncate_table, signup_facebook_request_data, mock_facebook, welcome_message):
    truncate_table(FruitUser)
    request_data = signup_facebook_request_data()

    mock_facebook()

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    user = FruitUser.objects.get(email=request_data["email"])
    token = Token.objects.get(user=user)

    expected = {
        "id": user.id,
        "token": token.key,
    }

    assert response.json() == expected
    assert user.facebook.fcb_id == request_data["fcb_id"]
    assert user.facebook.fcb_token == request_data["fcb_token"]

    assert user.messages.count() == 1
    assert user.messages.last().text_formatted == welcome_message()


@pytest.mark.django_db
def test_facebook_signup_user_exists(client, truncate_table, new_user, signup_facebook_request_data, mock_facebook):
    truncate_table(FruitUser)
    existing_user = new_user(is_email_verified=False)
    request_data = signup_facebook_request_data(email=existing_user.email)

    mock_facebook()

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    existing_user = FruitUser.objects.get(email=request_data["email"])
    token = Token.objects.get(user=existing_user)

    expected = {
        "id": existing_user.id,
        "token": token.key,
    }

    assert response.json() == expected
    assert existing_user.facebook.fcb_id == request_data["fcb_id"]
    assert existing_user.facebook.fcb_token == request_data["fcb_token"]
    assert existing_user.is_email_verified is True

    assert existing_user.messages.count() == 1


def test_facebook_signup_fcb_info_exists(client, new_facebook_info, signup_facebook_request_data, mock_facebook):
    fcb_info = new_facebook_info()
    request_data = signup_facebook_request_data(
        email=fcb_info.user.email, fcb_id=fcb_info.fcb_id, fcb_token="new_token"
    )

    mock_facebook()

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK

    user = FruitUser.objects.get(email=request_data["email"])
    token = Token.objects.get(user=user)

    expected = {
        "id": user.id,
        "token": token.key,
    }

    assert response.json() == expected
    assert user.facebook.fcb_id == request_data["fcb_id"]
    assert user.facebook.fcb_token == request_data["fcb_token"]

    assert user.messages.count() == 1


@pytest.mark.parametrize(
    "missing_arg, error_msg",
    [
        ("email", {"email": ["This field is required."]}),
        ("fcb_id", {"fcb_id": ["This field is required."]}),
        ("fcb_token", {"fcb_token": ["This field is required."]}),
    ],
)
def test_facebook_signup_missing_args(client, signup_facebook_request_data, missing_arg, error_msg):
    request_data = signup_facebook_request_data()
    request_data.pop(missing_arg)

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize("bad_args, error_msg", SIGNUP_BAD_ARGS)
def test_facebook_signup_bad_args(client, signup_facebook_request_data, bad_args, error_msg):
    request_data = signup_facebook_request_data(**bad_args)

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_facebook_signup_fcb_verification_failed(client, signup_facebook_request_data, mock_facebook):
    request_data = signup_facebook_request_data()

    mock_facebook(fails=True)

    response = client.post(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"non_field_errors": ["Facebook verification failed: Facebook error"]}


@pytest.mark.parametrize("bad_method", HTTP_METHODS - {"post", "options"})
@pytest.mark.django_db
def test_facebook_signup_bad_methods(
    client, signup_facebook_request_data, mock_facebook, bad_method, bad_method_response
):
    request_data = signup_facebook_request_data()

    mock_facebook()

    response = getattr(client, bad_method)(
        reverse("api:signup-fcb"),
        request_data,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
