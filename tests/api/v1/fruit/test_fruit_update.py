import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from . import BAD_FRUIT_CRUD_ARGS, fruit_to_verbose_data


def test_fruit_update(client, random_password, new_user, new_fruit, fruit_request_data):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)

    assert client.login(username=author.username, password=password)

    request_data = fruit_request_data()
    response = client.patch(
        reverse("api:fruit-detail", args=[fruit.id]),
        json.dumps(request_data),
        content_type="application/json",
    )
    modified_data = {
        **fruit_to_verbose_data(fruit, response),
        **request_data,
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == modified_data


@pytest.mark.parametrize("bad_args, error_msg", BAD_FRUIT_CRUD_ARGS)
def test_fruit_update_bad_args(client, random_password, new_user, new_fruit, fruit_request_data, bad_args, error_msg):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)

    assert client.login(username=author.username, password=password)

    response = client.patch(
        reverse("api:fruit-detail", args=[fruit.id]),
        json.dumps(fruit_request_data(**bad_args)),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_fruit_update_unauthenticated(client, new_fruit, fruit_request_data):
    fruit = new_fruit()

    response = client.patch(
        reverse("api:fruit-detail", args=[fruit.id]),
        json.dumps(fruit_request_data()),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Authentication credentials were not provided."}


def test_fruit_update_unauthorized(client, random_password, new_user, new_fruit, fruit_request_data):
    password = random_password()
    different_user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=different_user.username, password=password)

    response = client.patch(
        reverse("api:fruit-detail", args=[fruit.id]),
        json.dumps(fruit_request_data()),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "You do not have permission to perform this action."}
