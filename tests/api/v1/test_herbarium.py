from functools import partial

import funcy
import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from .utils import sort_by_key
from .utils.data import herbarium_item_to_data


@pytest.mark.django_db
def test_herbarium_list(client, all_herbarium_items):
    expected = map(herbarium_item_to_data, all_herbarium_items)
    # We omit photos because there are no files associated with photos during testing.
    without_photos = partial(funcy.map, partial(funcy.omit, keys=['photo']))
    response = client.get(reverse('api:herbarium-list') + '?raw')

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_key('kind_key', without_photos(response.json())) == sort_by_key('kind_key', expected)
