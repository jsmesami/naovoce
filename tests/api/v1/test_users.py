from functools import partial
from operator import itemgetter

from rest_framework.reverse import reverse
from rest_framework import status

from ..utils import render_url


def user_to_data(user, response):
    return {
        'id': user.id,
        'username': user.username,
        'url': render_url(response, 'api:users-detail', user.id),
    }


def test_users_list(client, new_user):
    new_users = [new_user() for _ in range(5)] + [
        new_user(is_email_verified=False, is_active=True),  # Additional unverified user
        new_user(is_email_verified=True, is_active=False),  # Additional inactive user
    ]

    response = client.get(reverse('api:users-list'))

    sort_by_id = partial(sorted, key=itemgetter('id'))
    expected = map(partial(user_to_data, response=response), new_users)

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_id(response.json()) == sort_by_id(expected)
