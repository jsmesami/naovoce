import pytest

from herbarium.models import Herbarium


@pytest.fixture
@pytest.mark.django_db
def all_herbarium_items():
    return Herbarium.objects.select_related("kind").prefetch_related("seasons")
