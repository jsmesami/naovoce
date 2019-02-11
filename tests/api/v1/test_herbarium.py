from functools import partial
from operator import itemgetter

import funcy
import pytest

from rest_framework.reverse import reverse
from rest_framework import status


def season_to_data(season):
    return {
        'part': season.part,
        'start': season.start,
        'duration': season.duration,
    }


def herbarium_item_to_data(item):
    return {
        'name': item.name,
        'latin_name': item.latin_name,
        'description': item.description,
        'kind_key': item.kind.key,
        'seasons': list(map(season_to_data, item.seasons.all())),
        # We omit photos because there are no files associated with photos during testing.
    }


@pytest.mark.django_db
def test_herbarium_list(client, all_herbarium_items):
    expected = map(herbarium_item_to_data, all_herbarium_items)
    sort_by_kind_key = partial(sorted, key=itemgetter('kind_key'))
    without_photos = partial(funcy.map, partial(funcy.omit, keys=['photo']))
    response = client.get(reverse('api:herbarium-list') + '?raw')

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_kind_key(without_photos(response.json())) == sort_by_kind_key(expected)
