import json
from functools import partial
from operator import itemgetter

import funcy
from libfaketime import fake_time
import pytest
from datetime import date, timedelta
from rest_framework.fields import DateTimeField
from rest_framework.reverse import reverse
from rest_framework import status

from fruit.models import Fruit
from ..utils import render_url


def format_coord(coord):
    return '{:.10f}'.format(coord)


def format_time(time):
    return DateTimeField(format='%Y-%m-%d %H:%M:%S').to_representation(time)


def fruit_to_data(fruit, response):
    return {
        'id': fruit.id,
        'lat': format_coord(fruit.position.y),
        'lng': format_coord(fruit.position.x),
        'kind': fruit.kind.key,
        'time': format_time(fruit.created),
        'url': render_url(response, 'api:fruit-detail', fruit.id),
     }


def fruit_to_verbose_data(fruit, response):
    return {
        'id': fruit.id,
        'lat': format_coord(fruit.position.y),
        'lng': format_coord(fruit.position.x),
        'kind': fruit.kind.key,
        'time': format_time(fruit.created),
        'url': render_url(response, 'api:fruit-detail', fruit.id),
        'description': fruit.description,
        'user': {
            'id': fruit.user.id,
            'username': fruit.user.username,
            'url': render_url(response, 'api:users-detail', fruit.user.id),
        },
        'images_count': 0,
        'images': render_url(response, 'api:image-list', 'fruit', fruit.id)
    }


BAD_FRUIT_CRUD_ARGS = [
    ({'kind': 'nonexistent'}, {'kind': ['nonexistent is not a valid Kind key.']}),
    ({'kind': ''}, {'kind': ['This field may not be null.']}),
    ({'lat': 'NaN'}, {'lat': ['A valid number is required.']}),
    ({'lat': ''}, {'lat': ['A valid number is required.']}),
    ({'lat': '60.1234564567890'}, {'lat': ['Ensure that there are no more than 13 digits in total.']}),
    ({'lng': 'NaN'}, {'lng': ['A valid number is required.']}),
    ({'lng': ''}, {'lng': ['A valid number is required.']}),
    ({'lng': '60.1234564567890'}, {'lng': ['Ensure that there are no more than 13 digits in total.']}),
]


def is_fruit_list_valid(instances, response):
    expected = map(partial(fruit_to_data, response=response), instances)
    sort_by_id = partial(sorted, key=itemgetter('id'))

    return sort_by_id(expected) == sort_by_id(response.json())


@pytest.mark.django_db
def test_fruit_list(client, truncate_table, new_fruit_list):
    length = 5
    truncate_table(Fruit)
    instances = new_fruit_list(length)
    response = client.get(reverse('api:fruit-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    assert is_fruit_list_valid(instances, response)


@pytest.mark.django_db
def test_fruit_list_filtering(client, truncate_table, all_kinds, new_user, new_fruit_list):
    kind_a = all_kinds[1]
    kind_b = all_kinds[2]
    user_a = new_user()
    user_b = new_user()

    truncate_table(Fruit)
    instances_a = new_fruit_list(2, kind=kind_a, user=user_a)
    instances_b = new_fruit_list(2, kind=kind_a, user=user_b)
    instances_c = new_fruit_list(2, kind=kind_b, user=user_a)
    instances_d = new_fruit_list(2, kind=kind_b, user=user_b)

    scenarios = (
        (instances_a, {'kind': kind_a.key, 'user': user_a.id}, 2),
        (instances_b, {'kind': kind_a.key, 'user': user_b.id}, 2),
        (instances_c, {'kind': kind_b.key, 'user': user_a.id}, 2),
        (instances_d, {'kind': kind_b.key, 'user': user_b.id}, 2),
        (instances_a + instances_b, {'kind': kind_a.key}, 4),
        (instances_c + instances_d, {'kind': kind_b.key}, 4),
        (instances_a + instances_c, {'user': user_a.id}, 4),
        (instances_b + instances_d, {'user': user_b.id}, 4),
    )

    for instances, params, length in scenarios:
        response = client.get(reverse('api:fruit-list'), params)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == length
        assert is_fruit_list_valid(instances, response)


@pytest.mark.django_db
def test_fruit_list_pagination(client, truncate_table, new_fruit_list):
    length = 8
    step = 2
    truncate_table(Fruit)
    new_fruit_list(length)
    list_url = reverse('api:fruit-list')

    for offset in range(0, length, step):
        response = client.get(list_url, {'limit': step, 'offset': offset})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == length
        assert len(response.data['results']) == step

    response = client.get(list_url, {'limit': step, 'offset': length})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == length
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_fruit_list_difference(client, truncate_table, new_fruit_list):
    truncate_table(Fruit)
    old = (date.today() - timedelta(days=6)).strftime('%Y-%m-%d')
    new = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d')

    with fake_time(old):
        f1, *_ = new_fruit_list(4)

    with fake_time(new):
        f2, f3 = new_fruit_list(2)
        f2.deleted = True
        f2.save()
        f1.save()

    response = client.get(reverse('api:fruit-diff', args=[new]))

    assert response.status_code == status.HTTP_200_OK
    assert Fruit.objects.count() == 6

    diff = response.json()
    scenarios = (
        ('created', f3),
        ('deleted', f2),
        ('updated', f1),
    )
    for state, instance in scenarios:
        assert len(diff[state]) == 1
        assert diff[state][0]['id'] == instance.id


def test_fruit_detail(client, random_kind, new_fruit, new_user):
    kind = random_kind()
    fruit = new_fruit(kind=kind, description='fruit')

    response = client.get(reverse('api:fruit-detail', args=[fruit.id]))

    assert response.status_code == status.HTTP_200_OK
    assert fruit_to_verbose_data(fruit, response) == response.json()


@pytest.mark.django_db
def test_fruit_detail_nonexistent_fruit(client, truncate_table):
    truncate_table(Fruit)

    response = client.get(reverse('api:fruit-detail', args=[1]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found.'}


def test_fruit_create(client, random_password, new_user, fruit_request_data):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    request_data = fruit_request_data()
    response = client.post(reverse('api:fruit-list'), request_data)

    assert response.status_code == status.HTTP_201_CREATED

    created = response.json()

    assert user.username == created['user']['username']
    assert request_data == {
        'kind': created['kind'],
        'lat': created['lat'],
        'lng': created['lng'],
        'description': created['description'],
    }


@pytest.mark.parametrize('bad_args, error_msg', BAD_FRUIT_CRUD_ARGS)
def test_fruit_create_bad_args(client, random_password, new_user, fruit_request_data, bad_args, error_msg):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-list'), fruit_request_data(**bad_args))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


@pytest.mark.parametrize(
    'missing_arg, error_msg', [
        ('kind', {'kind': ['This field is required.']}),
        ('lat', {'lat': ['This field is required.']}),
        ('lng', {'lng': ['This field is required.']}),
    ]
)
def test_fruit_create_missing_args(client, random_password, new_user, fruit_request_data, missing_arg, error_msg):
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-list'), funcy.omit(fruit_request_data(), [missing_arg]))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_fruit_create_unauthenticated(client, fruit_request_data):
    response = client.post(reverse('api:fruit-list'), fruit_request_data())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_fruit_create_unauthorized(client, random_password, new_user, fruit_request_data):
    password = random_password()
    user = new_user(password=password, is_email_verified=False)

    assert client.login(username=user.username, password=password)

    response = client.post(reverse('api:fruit-list'), fruit_request_data())

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}


def test_fruit_update(client, random_password, new_user, new_fruit, fruit_request_data):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)

    assert client.login(username=author.username, password=password)

    request_data = fruit_request_data()
    response = client.patch(
        reverse('api:fruit-detail', args=[fruit.id]),
        json.dumps(request_data),
        content_type='application/json'
    )
    modified_data = {
        **fruit_to_verbose_data(fruit, response),
        **request_data,
    }

    assert response.status_code == status.HTTP_200_OK
    assert modified_data == response.json()


@pytest.mark.parametrize('bad_args, error_msg', BAD_FRUIT_CRUD_ARGS)
def test_fruit_update_bad_args(client, random_password, new_user, new_fruit, fruit_request_data, bad_args, error_msg):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)

    assert client.login(username=author.username, password=password)

    response = client.patch(
        reverse('api:fruit-detail', args=[fruit.id]),
        json.dumps(fruit_request_data(**bad_args)),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg


def test_fruit_update_unauthenticated(client, new_fruit, fruit_request_data):
    fruit = new_fruit()

    response = client.patch(
        reverse('api:fruit-detail', args=[fruit.id]),
        json.dumps(fruit_request_data()),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_fruit_update_unauthorized(client, random_password, new_user, new_fruit, fruit_request_data):
    password = random_password()
    different_user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=different_user.username, password=password)

    response = client.patch(
        reverse('api:fruit-detail', args=[fruit.id]),
        json.dumps(fruit_request_data()),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}


def test_fruit_delete(client, random_password, new_user, new_fruit):
    password = random_password()
    author = new_user(password=password)
    fruit = new_fruit(user=author)
    detail_url = reverse('api:fruit-detail', args=[fruit.id])
    request_args = {'why_deleted': 'because'}

    assert client.login(username=author.username, password=password)

    response = client.delete(detail_url, json.dumps(request_args), content_type='application/json')

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
        response = action(detail_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Cannot update once deleted object.'}


def test_fruit_delete_unauthenticated(client, new_fruit):
    fruit = new_fruit()
    response = client.delete(reverse('api:fruit-detail', args=[fruit.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_fruit_delete_unauthorized(client, random_password, new_user, new_fruit):
    password = random_password()
    different_user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=different_user.username, password=password)

    response = client.delete(reverse('api:fruit-detail', args=[fruit.id]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}
