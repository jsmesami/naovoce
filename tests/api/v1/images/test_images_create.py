from urllib.parse import urlencode

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from . import CREATE_IMAGE_BAD_ARGS, image_to_data
from fruit.models import Image, Fruit


def test_image_create(client, new_fruit_username_password, small_image_jpg):
    fruit, username, password = new_fruit_username_password()

    request_data = {
        'image': small_image_jpg(),
        'caption': 'caption',
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED

    created_image_response = response.json()
    created_image = Image.objects.get(pk=created_image_response['id'])

    expected = {
        **image_to_data(created_image, response),
        'caption': request_data['caption'],
    }

    assert created_image_response == expected

    modified_fruit = Fruit.objects.get(pk=fruit.id)

    assert modified_fruit.images.count() == 1
    assert image_to_data(modified_fruit.images.first(), response) == expected


def test_image_create_urlencoded(client, new_fruit_username_password, small_image_jpg):
    fruit, username, password = new_fruit_username_password()

    request_data = {
        'image': small_image_jpg(),
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        urlencode(request_data),
        content_type='application/x-www-form-urlencoded',
    )

    assert response.status_code == status.HTTP_201_CREATED

    created_image_response = response.json()
    created_image = Image.objects.get(pk=created_image_response['id'])

    assert created_image_response == image_to_data(created_image, response)


@pytest.mark.parametrize('bad_args, error_msg', CREATE_IMAGE_BAD_ARGS)
def test_image_create_bad_args(client, new_fruit_username_password, small_image_jpg, bad_args, error_msg):
    fruit, username, password = new_fruit_username_password()

    request_data = {
        'image': small_image_jpg(),
        'caption': 'caption',
        **bad_args,
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_image_create_image_too_large(client, new_fruit_username_password, larger_image_jpg):
    fruit, username, password = new_fruit_username_password()
    request_data = {
        'image': larger_image_jpg(),
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'image': ['Uploaded file size exceeds 0.00 MB.']}


def test_image_create_unsupported_content_type(client, new_fruit_username_password, small_image_png):
    fruit, username, password = new_fruit_username_password()
    request_data = {
        'image': small_image_png(),
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'image': ['Only JPEG files are allowed.']}


def test_image_create_missing_args(client, new_fruit_username_password, small_image_jpg):
    fruit, username, password = new_fruit_username_password()

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        {},
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'image': ['No file was submitted.']}


def test_image_create_unauthenticated(client, new_fruit, small_image_jpg):
    fruit = new_fruit()
    request_data = {
        'image': small_image_jpg(),
    }

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        request_data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
