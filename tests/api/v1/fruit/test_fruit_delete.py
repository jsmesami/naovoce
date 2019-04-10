import json

import funcy
from rest_framework.reverse import reverse
from rest_framework import status

from . import fruit_to_verbose_data


def test_fruit_delete(client, random_password, new_user, new_fruit):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)
    detail_url = reverse('api:fruit-detail', args=[fruit.id])
    request_args = {'why_deleted': 'because'}

    assert client.login(username=author.username, password=password)

    response = client.delete(
        detail_url,
        json.dumps(request_args),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # We are still able to fetch the data, but in a different shape
    response = client.get(detail_url)
    response_data = response.json()
    expected = {
        **fruit_to_verbose_data(fruit, response),
        **request_args,
        'deleted': True,
        'time': response_data['time'],
    }

    assert response_data == funcy.omit(expected, ['lat', 'lng', 'images_count'])


def test_fruit_modify_deleted(client, random_password, new_user, new_fruit):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author, deleted=True)
    detail_url = reverse('api:fruit-detail', args=[fruit.id])

    assert client.login(username=author.username, password=password)

    for action in (client.delete, client.patch, client.put):
        response = action(detail_url, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Cannot update once deleted object.'}


def test_fruit_modify_deleted_kind(client, random_password, new_user, new_fruit, deleted_kinds):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(kind=deleted_kinds().first(), user=author, deleted=False)
    detail_url = reverse('api:fruit-detail', args=[fruit.id])

    assert client.login(username=author.username, password=password)

    for action in (client.delete, client.patch, client.put):
        response = action(detail_url, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Cannot update once deleted object.'}


def test_fruit_delete_unauthenticated(client, new_fruit):
    fruit = new_fruit()
    response = client.delete(
        reverse('api:fruit-detail', args=[fruit.id]),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_fruit_delete_unauthorized(client, random_password, new_user, new_fruit):
    password = random_password()
    different_user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=different_user.username, password=password)

    response = client.delete(
        reverse('api:fruit-detail', args=[fruit.id]),
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}
