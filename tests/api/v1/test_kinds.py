from operator import itemgetter

import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from .utils import sort_by_key
from .utils.data import kind_to_data


@pytest.mark.django_db
def test_kinds_list(client, valid_kinds):
    expected = map(kind_to_data, valid_kinds())
    response = client.get(reverse('api:kinds-list'))

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_key('key', response.json()) == sort_by_key('key', expected)


@pytest.mark.django_db
def test_kinds_list_some_deleted(client, deleted_kinds_keys):
    response = client.get(reverse('api:kinds-list'))

    assert response.status_code == status.HTTP_200_OK

    deleted_kinds_keys = set(deleted_kinds_keys())
    listed_kinds_keys = set(map(itemgetter('key'), response.json()))

    assert len(deleted_kinds_keys) > 0
    assert len(listed_kinds_keys) > 0
    assert (deleted_kinds_keys & listed_kinds_keys) == set()
