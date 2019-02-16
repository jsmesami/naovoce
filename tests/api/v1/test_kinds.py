import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from .utils import sort_by_key
from .utils.data import kind_to_data


@pytest.mark.django_db
def test_kinds_list(client, all_kinds):
    expected = map(kind_to_data, all_kinds)
    response = client.get(reverse('api:kinds-list'))

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_key('key', response.json()) == sort_by_key('key', expected)
