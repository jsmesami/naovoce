import json
from functools import partial
from urllib.parse import urlencode

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from fruit.models import Image, Fruit
from .utils import sort_by_key
from .utils.data import image_to_data

CAPTION_MAX_LENGTH = Image._meta.get_field('caption').max_length
CREATE_IMAGE_BAD_ARGS = [
    ({'caption': 'c' * (CAPTION_MAX_LENGTH + 1)},
     {'caption': ['Ensure this field has no more than {} characters.'.format(CAPTION_MAX_LENGTH)]}),
    ({'caption': None},
     {'caption': ['This field may not be null.']}),
    ({'image': None},
     {'image': ['This field may not be null.']}),
    ({'image': 'rubbish'},
     {'image': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']}),
]


@pytest.fixture
def new_fruit_username_password(new_fruit, random_password, new_user):
    def closure():
        password = random_password()
        return new_fruit(), new_user(password=password).username, password

    return closure


def test_images_list(client, new_fruit_list, new_images_list):
    length = 2
    fruit1, fruit2, fruit3 = new_fruit_list(3)
    images1 = new_images_list(length, fruit=fruit1)
    images2 = new_images_list(length, fruit=fruit2)

    response = client.get(reverse('api:image-list', args=[fruit1.id]))

    expected = map(partial(image_to_data, response=response), images1)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == length
    assert sort_by_key('id', response.json()) == sort_by_key('id', expected)

    response = client.get(reverse('api:image-list', args=[fruit2.id]))

    expected = map(partial(image_to_data, response=response), images2)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == length
    assert sort_by_key('id', response.json()) == sort_by_key('id', expected)

    response = client.get(reverse('api:image-list', args=[fruit3.id]))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.parametrize('caption', ('c' * CAPTION_MAX_LENGTH, ''))
def test_image_create(client, new_fruit_username_password, small_image_jpg, caption):
    fruit, username, password = new_fruit_username_password()

    request_data = {
        'image': small_image_jpg(),
        'caption': caption,
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        json.dumps(request_data),
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
    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED

    created_image_response = response.json()
    created_image = Image.objects.get(pk=created_image_response['id'])

    assert created_image_response == image_to_data(created_image, response)


@pytest.mark.parametrize('additional_args, error_msg', CREATE_IMAGE_BAD_ARGS)
def test_image_create_bad_args(client, new_fruit_username_password, small_image_jpg, additional_args, error_msg):
    fruit, username, password = new_fruit_username_password()

    request_data = {
        'image': small_image_jpg(),
        'caption': 'caption',
        **additional_args,
    }

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        json.dumps(request_data),
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
        json.dumps(request_data),
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
        json.dumps(request_data),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'image': ['Only JPEG files are allowed.']}


def test_image_create_missing_args(client, new_fruit_username_password, small_image_jpg):
    fruit, username, password = new_fruit_username_password()

    assert client.login(username=username, password=password)

    response = client.post(
        reverse('api:image-list', args=[fruit.id]),
        json.dumps({}),
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
        json.dumps(request_data),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_image_delete(client, random_password, new_user, new_image):
    password = random_password()
    user = new_user(password=password)
    image = new_image(author=user)

    assert client.login(username=user.username, password=password)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_image_delete_unauthenticated(client, random_password, new_user, new_image):
    user = new_user()
    image = new_image(author=user)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_image_delete_unauthorized(client, random_password, new_user, new_image):
    image = new_image()
    password = random_password()
    different_user = new_user(password=password)

    assert client.login(username=different_user.username, password=password)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}
