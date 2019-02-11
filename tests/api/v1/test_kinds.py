from functools import partial
from operator import itemgetter

import pytest

from rest_framework.reverse import reverse
from rest_framework import status


def kind_to_data(kind):
    return {
        'key': kind.key,
        'name': kind.name,
        'col': kind.color,
        'cls': kind.cls_name,
    }


@pytest.mark.django_db
def test_kinds_list(client, all_kinds):
    expected = map(kind_to_data, all_kinds)
    sort_by_key = partial(sorted, key=itemgetter('key'))
    response = client.get(reverse('api:kinds-list'))

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_key(expected) == sort_by_key(response.json())
