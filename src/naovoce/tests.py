from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import transaction
from rest_framework.test import APITestCase

from user.models import FruitUser
from fruit.models import Kind, Fruit


class NaovoceAPITestCase(APITestCase):
    """
    Provides base for API tests
    """
    fixtures = 'kinds.json',

    kind_keys = (
        'a1e4',  # Apple Tree
        'a3b8',  # Pear Tree
        'a412',  # Herry Tree
        'a3a2',  # Sour Cherry
    )
    kinds = Kind.objects.filter(key__in=kind_keys)

    fruit_data = {
        'kind': kind_keys[0],
        'lat': Decimal('60.123456'),
        'lng': Decimal('50.123456'),
    }
    fruit_set = None  # all fruit
    fruit = None      # one fruit

    yuri = None       # user 1
    lara = None       # user 2
    user_password = 'sesame123'

    @classmethod
    def setUpTestData(cls):
        # create 2 test users
        cls.yuri = FruitUser.objects.create_user(
            username='yuri',
            email='yuri@example.com',
            password=cls.user_password,
        )
        cls.lara = FruitUser.objects.create_user(
            username='lara',
            email='lara@example.com',
            password=cls.user_password,
        )

        # create some fruit
        with transaction.atomic():
            cls.fruit_list = [
                Fruit.objects.create(
                    latitude=cls.fruit_data['lat'],
                    longitude=cls.fruit_data['lng'],
                    kind=kind,
                    user=cls.yuri,
                )
                for kind in cls.kinds
            ]

        cls.fruit = cls.fruit_list[0]

        cls.fruit_list_url = reverse('api:fruit-list')
        cls.fruit_url = reverse('api:fruit-detail', args=[cls.fruit.pk])

    def login(self, who):
        self.client.login(username=who.username, password=self.user_password)

    def assertIsValidUrl(self, url, view_name, *args):
        regex = r'^https?://.*{expected_url}$'.format(
            expected_url=reverse(view_name, args=args)
        )
        self.assertRegex(url, regex)

    def assertIsValidUser(self, user_data):
        self.assertIsNotNone(user_data)
        self.assertTrue(int(user_data['id']))
        self.assertIsNotNone(user_data['username'])
        self.assertIsValidUrl(user_data['url'], 'api:users-detail', user_data['id'])

    def assertIsSameUser(self, user_data, user_obj):
        self.assertEqual(user_data['id'], user_obj.id)
        self.assertEqual(user_data['username'], user_obj.username)
        self.assertIsValidUrl(user_data['url'], 'api:users-detail', user_obj.id)
