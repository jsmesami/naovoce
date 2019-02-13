from datetime import date, timedelta
from functools import partial
from operator import itemgetter

from libfaketime import fake_time
import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from user.models import FruitUser
from ..utils import render_url


def user_to_data(user, response):
    return {
        'id': user.id,
        'username': user.username,
        'url': render_url(response, 'api:users-detail', user.id),
    }


def top_user_to_data(user, response):
    return {
        **user_to_data(user, response),
        'fruit_count': user.fruits.count(),
        'avatar': user.get_avatar(response.renderer_context['request']),
    }


def user_detail_to_data(user, response):
    return {
        **top_user_to_data(user, response),
        'fruit': render_url(response, 'api:fruit-list') + '?user={}'.format(user.id),
        'active': user.is_active,
        'motto': user.motto,
        'url': render_url(response, 'api:users-detail', user.id),
    }


@pytest.mark.django_db
def test_users_list(client, truncate_table, new_random_user_list, new_user):
    truncate_table(FruitUser)

    new_users = new_random_user_list(5) + [
        new_user(is_email_verified=False, is_active=True),  # Additional unverified user
        new_user(is_email_verified=True, is_active=False),  # Additional inactive user
    ]

    response = client.get(reverse('api:users-list'))

    sort_by_id = partial(sorted, key=itemgetter('id'))
    expected = map(partial(user_to_data, response=response), new_users)

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_id(response.json()) == sort_by_id(expected)


@pytest.mark.django_db
def test_users_list_pagination(client, truncate_table, new_random_user_list):
    length = 8
    step = 2
    truncate_table(FruitUser)
    new_random_user_list(length)

    users_list_url = reverse('api:users-list')

    for offset in range(0, length, step):
        response = client.get(users_list_url, {'limit': step, 'offset': offset})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == length
        assert len(response.data['results']) == step

    response = client.get(users_list_url, {'limit': step, 'offset': length})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == length
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_users_list_top_users(client, truncate_table, new_fruit_list, new_user):
    truncate_table(FruitUser)

    user4 = new_user(username='aaa')
    user3 = new_user(username='ccc')
    user2 = new_user(username='bbb')
    user1 = new_user(username='ddd')

    new_fruit_list(1, user=user4)
    new_fruit_list(2, user=user3)
    new_fruit_list(2, user=user2)
    new_fruit_list(3, user=user1)

    response = client.get(reverse('api:users-list-top'))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == list(map(partial(top_user_to_data, response=response), (user1, user2, user3, user4)))


@pytest.mark.django_db
def test_users_list_top_users_last_month(client, new_user, new_fruit_list):
    user4 = new_user(username='aaa')
    user3 = new_user(username='ccc')
    user2 = new_user(username='bbb')
    user1 = new_user(username='ddd')

    month_ago = (date.today() - timedelta(days=365 / 12 + 1)).strftime('%Y-%m-%d')
    now = date.today().strftime('%Y-%m-%d')

    with fake_time(month_ago):
        new_fruit_list(3, user=user1)

    with fake_time(now):
        new_fruit_list(1, user=user4)
        new_fruit_list(2, user=user3)
        new_fruit_list(2, user=user2)

    response = client.get(reverse('api:users-list-top-last-month'))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == list(map(partial(top_user_to_data, response=response), (user2, user3, user4)))


def test_user_detail(client, new_user):
    user = new_user()
    user.motto = 'For the next generation of big businesses'
    user.save()

    response = client.get(reverse('api:users-detail', args=[user.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_detail_to_data(user, response)
