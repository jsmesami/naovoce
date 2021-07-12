import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from fruit.models import Fruit

from . import fruit_to_verbose_data


def test_fruit_detail(client, random_valid_kind, new_fruit):
    kind = random_valid_kind()
    fruit = new_fruit(kind=kind, description="fruit")

    response = client.get(reverse("api:fruit-detail", args=[fruit.id]))

    assert response.status_code == status.HTTP_200_OK
    assert fruit_to_verbose_data(fruit, response) == response.json()


@pytest.mark.django_db
def test_fruit_detail_nonexistent_fruit(client, truncate_table):
    truncate_table(Fruit)

    response = client.get(reverse("api:fruit-detail", args=[1]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found."}
