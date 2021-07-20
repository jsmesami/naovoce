import os
import random
import string
from datetime import date

import pytest
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.db import connection
from django.utils.formats import date_format
from django.utils.html import format_html
from psycopg2.extensions import AsIs

from fruit.models import Fruit, Kind
from user.models.user import WELCOME_MESSAGE


@pytest.fixture(scope="session")
@pytest.mark.django_db
def django_db_setup(django_db_blocker):
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "fixtures"))

    with django_db_blocker.unblock():
        call_command("loaddata", os.path.join(fixtures_dir, "kinds.json"))
        call_command("loaddata", os.path.join(fixtures_dir, "sites.json"))

        # Delete one kind:
        kind = random.choice(Kind.objects.valid())
        kind.deleted = True
        kind.save()


@pytest.fixture(autouse=True)
def set_default_language(settings):
    settings.LANGUAGE_CODE = "en"


@pytest.fixture(autouse=True)
def set_media_root(settings):
    settings.MEDIA_ROOT = os.path.join(settings.PROJECT_ROOT, "tests/media")


@pytest.fixture
@pytest.mark.django_db
def truncate_table():
    return lambda model: connection.cursor().execute("TRUNCATE TABLE %s CASCADE", [AsIs(model._meta.db_table)])


@pytest.fixture
def random_string():
    return lambda length: "".join(random.choice(string.ascii_lowercase) for _ in range(length))


@pytest.fixture
def random_password(random_string):
    return lambda: random_string(8)


@pytest.fixture
def random_username(random_string):
    return lambda: random_string(8)


@pytest.fixture
def random_email(random_string):
    return lambda: "{}@{}.com".format(random_string(6), random_string(6))


@pytest.fixture()
def welcome_message():
    def closure():
        return format_html(
            "<span class='date'>{date}</span> {text}",
            date=date_format(date.today(), "SHORT_DATE_FORMAT", use_l10n=True),
            text=format_html(WELCOME_MESSAGE, url=settings.CODEX_URL),
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_user(django_user_model, random_username, random_email, random_password):
    def closure(**kwargs):
        is_active = kwargs.pop("is_active", True)

        user = django_user_model.objects.create_user(
            username=kwargs.pop("username", random_username()),
            email=kwargs.pop("email", random_email()),
            password=kwargs.pop("password", random_password()),
            is_email_verified=kwargs.pop("is_email_verified", True),
            **kwargs
        )

        if user.is_active != is_active:
            user.is_active = is_active
            user.save()

        return user

    return closure


@pytest.fixture
def user_auth(random_password, new_user):
    def closure(**kwargs):
        password = kwargs.pop("password", random_password())
        user = kwargs.pop("user", None) or new_user(password=password)
        return {
            "username": user.username,
            "password": password,
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_random_user_list(random_position, new_user):
    return lambda length: [new_user() for _ in range(length)]


@pytest.fixture
@pytest.mark.django_db
def valid_kinds():
    return lambda: Kind.objects.valid()  # pylint: disable=unnecessary-lambda


@pytest.fixture
@pytest.mark.django_db
def valid_kinds_keys(valid_kinds):
    return lambda: valid_kinds().values_list("key", flat=True)


@pytest.fixture
@pytest.mark.django_db
def random_valid_kind(valid_kinds_keys):
    return lambda: Kind.objects.get(key=random.choice(valid_kinds_keys()))


@pytest.fixture
@pytest.mark.django_db
def deleted_kinds():
    return lambda: Kind.objects.filter(deleted=True)


@pytest.fixture
@pytest.mark.django_db
def deleted_kinds_keys(deleted_kinds):
    return lambda: deleted_kinds().values_list("key", flat=True)


@pytest.fixture
def random_position():
    return lambda: Point(60 + random.random(), 50 + random.random())


@pytest.fixture
def fruit_request_data(valid_kinds_keys):
    def closure(**kwargs):
        return {
            "kind": kwargs.pop("kind", valid_kinds_keys()[0]),
            "lat": kwargs.pop("lat", "6{:0.10f}".format(random.random())),
            "lng": kwargs.pop("lng", "5{:0.10f}".format(random.random())),
            "description": kwargs.pop("description", "fruit"),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit(random_position, random_valid_kind, new_user):
    def closure(**kwargs):
        position = kwargs.pop("position", random_position())
        kind = kwargs.pop("kind", random_valid_kind())
        user = kwargs.pop("user", None) or new_user()

        return Fruit.objects.create(position=position, kind=kind, user=user, **kwargs)

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit_list(random_position, random_valid_kind, new_user):
    def closure(length, **kwargs):
        position = kwargs.pop("position", random_position())
        kind = kwargs.pop("kind", random_valid_kind())
        user = kwargs.pop("user", None) or new_user()

        return Fruit.objects.bulk_create(
            Fruit(position=position, kind=kind, user=user, **kwargs) for _ in range(length)
        )

    return closure


@pytest.fixture
def bad_method_response():
    def closure(method):
        return {"detail": 'Method "{method}" not allowed.'.format(method=method.upper())}

    return closure
