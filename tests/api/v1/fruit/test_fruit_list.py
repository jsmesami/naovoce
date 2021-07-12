from datetime import date, timedelta
from functools import partial

import pytest
from libfaketime import fake_time
from rest_framework import status
from rest_framework.reverse import reverse

from fruit.models import Fruit

from ..utils import sort_by_key
from . import fruit_to_data


@pytest.mark.django_db
def test_fruit_list(client, truncate_table, new_fruit_list):
    length = 5
    truncate_table(Fruit)
    instances = new_fruit_list(length)

    response = client.get(reverse("api:fruit-list"))

    expected = map(partial(fruit_to_data, response=response), instances)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == length
    assert sort_by_key("id", expected) == sort_by_key("id", response.json())


@pytest.mark.django_db
def test_fruit_list_filtering(client, truncate_table, valid_kinds, new_user, new_fruit_list):
    kinds = valid_kinds()
    kind_a = kinds[1]
    kind_b = kinds[2]
    user_a = new_user()
    user_b = new_user()

    truncate_table(Fruit)
    instances_a = new_fruit_list(2, kind=kind_a, user=user_a)
    instances_b = new_fruit_list(2, kind=kind_a, user=user_b)
    instances_c = new_fruit_list(2, kind=kind_b, user=user_a)
    instances_d = new_fruit_list(2, kind=kind_b, user=user_b)

    scenarios = (
        (instances_a, {"kind": kind_a.key, "user": user_a.id}, 2),
        (instances_b, {"kind": kind_a.key, "user": user_b.id}, 2),
        (instances_c, {"kind": kind_b.key, "user": user_a.id}, 2),
        (instances_d, {"kind": kind_b.key, "user": user_b.id}, 2),
        (instances_a + instances_b, {"kind": kind_a.key}, 4),
        (instances_c + instances_d, {"kind": kind_b.key}, 4),
        (instances_a + instances_c, {"user": user_a.id}, 4),
        (instances_b + instances_d, {"user": user_b.id}, 4),
    )

    for instances, params, length in scenarios:
        response = client.get(reverse("api:fruit-list"), params)

        expected = map(partial(fruit_to_data, response=response), instances)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == length
        assert sort_by_key("id", expected) == sort_by_key("id", response.json())


@pytest.mark.django_db
def test_fruit_list_pagination(client, truncate_table, new_fruit_list):
    length = 8
    step = 2
    truncate_table(Fruit)
    new_fruit_list(length)
    list_url = reverse("api:fruit-list")

    for offset in range(0, length, step):
        response = client.get(list_url, {"limit": step, "offset": offset})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == length
        assert len(response.data["results"]) == step

    response = client.get(list_url, {"limit": step, "offset": length})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == length
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_fruit_list_difference(client, truncate_table, new_fruit_list):
    truncate_table(Fruit)
    old = (date.today() - timedelta(days=6)).strftime("%Y-%m-%d")
    new = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

    with fake_time(old):
        f1, *_ = new_fruit_list(4)

    with fake_time(new):
        f2, f3 = new_fruit_list(2)
        f2.deleted = True
        f2.save()
        f1.save()

    response = client.get(reverse("api:fruit-diff", args=[new]))

    assert response.status_code == status.HTTP_200_OK
    assert Fruit.objects.count() == 6

    diff = response.json()
    scenarios = (
        ("created", f3),
        ("deleted", f2),
        ("updated", f1),
    )
    for state, instance in scenarios:
        assert len(diff[state]) == 1
        assert diff[state][0]["id"] == instance.id


@pytest.mark.django_db
def test_fruit_list_difference_kind_deleted(client, truncate_table, deleted_kinds, new_fruit):
    truncate_table(Fruit)
    kind = deleted_kinds().first()
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    with fake_time(yesterday):
        fruit = new_fruit(kind=kind, deleted=False)

    response = client.get(reverse("api:fruit-diff", args=[yesterday]))

    assert response.status_code == status.HTTP_200_OK
    assert Fruit.objects.count() == 1

    diff = response.json()

    assert len(diff["deleted"]) == 1
    assert diff["deleted"][0]["id"] == fruit.id
