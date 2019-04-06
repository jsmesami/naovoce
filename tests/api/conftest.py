import base64
import os
import random
import string

import facebook
import pytest
from django.conf import settings

from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.db import connection
from psycopg2.extensions import AsIs

from herbarium.models import Herbarium
from fruit.models import Fruit, Kind, Image
from user.models import FacebookInfo

with open(os.path.join(settings.PROJECT_ROOT, 'tests/data/small_image.jpg'), 'rb') as image_file:
    SMALL_IMAGE_DATA_JPG = image_file.read()


with open(os.path.join(settings.PROJECT_ROOT, 'tests/data/larger_image.jpg'), 'rb') as image_file:
    LARGER_IMAGE_DATA_JPG = image_file.read()

FCB_ID = '110045436843169'
FCB_TOKEN = (
    'EAADvcY7nZCq8BAGbU0JMgZCaOPtQZBZBuioYJcIghkoFu2A26HWWzykYhcnVYY6ihNZBVh'
    'QlHFpnMeZBAhpobEA6bGTLbPw3Fqbfsv8SfgsP2augzlcWFcZCe2uDDs9DP6f3PNZBZAM0c'
    'OnwxdhzRorxugOfO1EHJuyw2jhcQMZCzJVCfhq8FWpb40CmFPwg1WNQbtktW11hOiggZDZD'
)


@pytest.fixture(scope='session')
@pytest.mark.django_db
def django_db_setup(django_db_blocker):
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'fixtures'))

    with django_db_blocker.unblock():
        call_command('loaddata', os.path.join(fixtures_dir, 'kinds.json'))
        call_command('loaddata', os.path.join(fixtures_dir, 'sites.json'))


@pytest.fixture(scope='session')
@pytest.mark.django_db
def delete_one_kind(random_valid_kind):
    kind = random_valid_kind()
    kind.deleted = True
    kind.save()


@pytest.fixture(autouse=True)
def set_default_language(settings):
    settings.LANGUAGE_CODE = 'en'


@pytest.fixture(autouse=True)
def set_media_root(settings):
    settings.MEDIA_ROOT = os.path.join(settings.PROJECT_ROOT, 'tests/media')


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
def signup_email_request_data(random_email, random_username, random_password):
    def closure(**kwargs):
        return {
            'email': kwargs.pop('email', random_email()),
            'username': kwargs.pop('username', random_username()),
            'password': kwargs.pop('password', random_password()),
        }

    return closure


@pytest.fixture
def signup_facebook_request_data(random_email):
    def closure(**kwargs):
        return {
            'email': kwargs.pop('email', random_email()),
            'fcb_id': kwargs.pop('fcb_id', FCB_ID),
            'fcb_token': kwargs.pop('fcb_token', FCB_ID),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_facebook_info(new_user):
    def closure(**kwargs):
        return FacebookInfo.objects.create(
            user=kwargs.pop('user', None) or new_user(),
            fcb_id=kwargs.pop('fcb_id', FCB_ID),
            fcb_token=kwargs.pop('fcb_token', FCB_TOKEN),
            **kwargs
        )

    return closure


@pytest.fixture
def mock_facebook(monkeypatch):
    def closure(fails=False, **overrides):
        def get_object(*args, **kwargs):
            if fails:
                raise facebook.GraphAPIError('Facebook error')

            return {
                'first_name': overrides.pop('first_name', 'Isaac'),
                'last_name': overrides.pop('last_name', 'Asimov'),
                'id': overrides.pop('fcb_id', FCB_ID),
                'picture': {
                    'data': {
                        'height': 200,
                        'is_silhouette': True,
                        'url': 'https://platform-lookaside.fbsbx.com/platform/profilepic/'
                               '?asid=110045436843169&height=200&width=200&ext=1556829832&hash=AeSLD93lbSjc5t96',
                        'width': 200,
                    },
                },
            }

        monkeypatch.setattr(facebook.GraphAPI, 'get_object', get_object)

    return closure


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


@pytest.fixture
@pytest.mark.django_db
def valid_kinds():
    return lambda: Kind.objects.valid()  # pylint: disable=unnecessary-lambda


@pytest.fixture
@pytest.mark.django_db
def valid_kinds_keys(valid_kinds):
    return lambda: valid_kinds().values_list('key', flat=True)


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
    return lambda: deleted_kinds().values_list('key', flat=True)


@pytest.fixture
def random_position():
    return lambda: Point(60 + random.random(), 50 + random.random())


@pytest.fixture
def fruit_request_data(valid_kinds_keys):
    def closure(**kwargs):
        return {
            'kind': kwargs.pop('kind', valid_kinds_keys()[0]),
            'lat': kwargs.pop('lat', '6{:0.10f}'.format(random.random())),
            'lng': kwargs.pop('lng', '5{:0.10f}'.format(random.random())),
            'description': kwargs.pop('description', 'fruit'),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit(random_position, random_valid_kind, new_user):
    def closure(**kwargs):
        position = kwargs.pop('position', random_position())
        kind = kwargs.pop('kind', random_valid_kind())
        user = kwargs.pop('user', None) or new_user()

        return Fruit.objects.create(
            position=position,
            kind=kind,
            user=user,
            **kwargs
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_fruit_list(random_position, random_valid_kind, new_user):
    def closure(length, **kwargs):
        position = kwargs.pop('position', random_position())
        kind = kwargs.pop('kind', random_valid_kind())
        user = kwargs.pop('user', None) or new_user()

        return Fruit.objects.bulk_create(
            Fruit(
                position=position,
                kind=kind,
                user=user,
                **kwargs
            )
            for _ in range(length)
        )

    return closure


@pytest.fixture
def small_image_jpg():
    return lambda: str(base64.b64encode(SMALL_IMAGE_DATA_JPG), encoding='ascii')


@pytest.fixture
def larger_image_jpg():
    return lambda: str(base64.b64encode(LARGER_IMAGE_DATA_JPG), encoding='ascii')


@pytest.fixture
def small_image_png():
    return lambda: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=='


@pytest.fixture
@pytest.mark.django_db
def new_image(small_image_jpg, new_user, random_string, new_fruit):
    def closure(**kwargs):
        image = kwargs.pop('image', None) or ContentFile(small_image_jpg(), name='image.jpg')
        author = kwargs.pop('author', None) or new_user()
        caption = kwargs.pop('caption', random_string(10))
        fruit = kwargs.pop('fruit', None) or new_fruit(user=author)

        return Image.objects.create(
            image=image,
            author=author,
            caption=caption,
            fruit=fruit,
            **kwargs
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_images_list(small_image_jpg, new_user, random_string, new_fruit):
    def closure(length, **kwargs):
        image = kwargs.pop('image', None) or ContentFile(small_image_jpg(), name='image.jpg')
        author = kwargs.pop('author', None) or new_user()
        caption = kwargs.pop('caption', random_string(10))
        fruit = kwargs.pop('fruit', None) or new_fruit(user=author)

        return Image.objects.bulk_create(
            Image(
                image=image,
                author=author,
                caption=caption,
                fruit=fruit,
                **kwargs
            )
            for _ in range(length)
        )

    return closure


@pytest.fixture
@pytest.mark.django_db
def all_herbarium_items():
    return Herbarium.objects.select_related('kind').prefetch_related('seasons')
