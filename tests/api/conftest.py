import os
import random
import string

import pytest

from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.db import connection
from psycopg2.extensions import AsIs

from herbarium.models import Herbarium
from fruit.models import Fruit, Kind


@pytest.fixture(scope='session')
@pytest.mark.django_db
def django_db_setup(django_db_blocker):
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'fixtures'))

    with django_db_blocker.unblock():
        call_command('loaddata', os.path.join(fixtures_dir, 'kinds.json'))
        call_command('loaddata', os.path.join(fixtures_dir, 'sites.json'))


@pytest.fixture(autouse=True)
def set_default_language(settings):
    settings.LANGUAGE_CODE = 'en'


@pytest.fixture
@pytest.mark.django_db
def truncate_table():
    return lambda model: connection.cursor().execute('TRUNCATE TABLE %s CASCADE', [AsIs(model._meta.db_table)])


@pytest.fixture
def random_string():
    return lambda length: ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@pytest.fixture
def random_password(random_string):
    return lambda: random_string(8)


@pytest.fixture
def random_username(random_string):
    return lambda: random_string(8)


@pytest.fixture
def random_email(random_string):
    return lambda: '{}@{}.com'.format(random_string(6), random_string(6))


@pytest.fixture
@pytest.mark.django_db
def new_user(django_user_model, random_username, random_email, random_password):
    def closure(**kwargs):
        is_active = kwargs.pop('is_active', True)

        user = django_user_model.objects.create_user(
            username=kwargs.pop('username', random_username()),
            email=kwargs.pop('email', random_email()),
            password=kwargs.pop('password', random_password()),
            is_email_verified=kwargs.pop('is_email_verified', True),
            **kwargs
        )

        if user.is_active != is_active:
            user.is_active = is_active
            user.save()

        return user

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_random_user_list(random_position, new_user):
    return lambda length: [new_user() for _ in range(length)]


@pytest.fixture(scope='session')
@pytest.mark.django_db
def all_kinds():
    return Kind.objects.all()


@pytest.fixture(scope='session')
@pytest.mark.django_db
def all_kinds_keys(all_kinds):
    return all_kinds.values_list('key', flat=True)


@pytest.fixture
@pytest.mark.django_db
def random_kind(all_kinds_keys):
    return lambda: Kind.objects.get(key=random.choice(all_kinds_keys))


@pytest.fixture
def random_position():
    return lambda: Point(60 + random.random(), 50 + random.random())


@pytest.fixture
def fruit_request_data(all_kinds_keys):
    def closure(**kwargs):
        return {
            'kind': kwargs.pop('kind', all_kinds_keys[0]),
            'lat': kwargs.pop('lat', '6{:0.10f}'.format(random.random())),
            'lng': kwargs.pop('lng', '5{:0.10f}'.format(random.random())),
            'description': kwargs.pop('description', 'fruit'),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit(random_position, random_kind, new_user):
    def closure(**kwargs):
        position = kwargs.pop('position', None)
        kind = kwargs.pop('kind', None)
        user = kwargs.pop('user', None)

        return Fruit.objects.create(
            position=position or random_position(),
            kind=kind or random_kind(),
            user=user or new_user(),
            **kwargs
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit_list(random_position, random_kind, new_user):
    def closure(length, **kwargs):
        position = kwargs.pop('position', None)
        kind = kwargs.pop('kind', None)
        user = kwargs.pop('user', None)

        return Fruit.objects.bulk_create(
            Fruit(
                position=position or random_position(),
                kind=kind or random_kind(),
                user=user or new_user(),
                **kwargs
            )
            for _ in range(length)
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def all_herbarium_items():
    return Herbarium.objects.select_related('kind').prefetch_related('seasons')
