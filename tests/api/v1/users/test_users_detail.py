import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from ..utils import HTTP_METHODS
from . import user_detail_to_data


def test_user_detail(client, new_user):
    user = new_user()
    user.motto = 'For the next generation of big businesses'
    user.save()

    response = client.get(reverse('api:users-detail', args=[user.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_detail_to_data(user, response)


@pytest.mark.parametrize('bad_method', HTTP_METHODS - {'get', 'options'})
def test_user_detail_bad_methods(client, new_user, bad_method, bad_method_response):
    user = new_user()

    response = getattr(client, bad_method)(reverse('api:users-detail', args=[user.id]))

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
