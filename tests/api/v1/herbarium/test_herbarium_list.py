from functools import partial

import funcy
import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from ..utils import HTTP_METHODS, sort_by_key
from . import herbarium_item_to_data


@pytest.mark.django_db
def test_herbarium_list(client, all_herbarium_items):
    expected = map(herbarium_item_to_data, all_herbarium_items)
    # We omit photos because there are no files associated with photos during testing.
    without_photos = partial(funcy.map, partial(funcy.omit, keys=["photo"]))
    response = client.get(reverse("api:herbarium-list") + "?raw")

    assert response.status_code == status.HTTP_200_OK
    assert sort_by_key("kind_key", without_photos(response.json())) == sort_by_key("kind_key", expected)


@pytest.mark.parametrize("bad_method", HTTP_METHODS - {"get", "options"})
def test_herbarium_list_bad_methods(client, all_herbarium_items, bad_method, bad_method_response):
    response = getattr(client, bad_method)(reverse("api:herbarium-list"))

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == bad_method_response(bad_method)
