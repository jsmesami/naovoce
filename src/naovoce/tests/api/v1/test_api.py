import datetime
from decimal import Decimal

from rest_framework import status

from . import NaovoceAPITestCase


class TestFruit(NaovoceAPITestCase):

    def assertIsValidFruit(self, fruit, user=None):
        if 'deleted' in fruit:
            self.assertTrue(fruit['deleted'])
            self.assertTrue('why_deleted' in fruit)
            self.assertIsNone(fruit.get('lat'))  # no location info
            self.assertIsNone(fruit.get('lng'))
        else:
            self.assertIsNone(fruit.get('why_deleted'))
            self.assertEqual(Decimal(fruit['lat']), self.fruit_data['lat'])
            self.assertEqual(Decimal(fruit['lng']), self.fruit_data['lng'])

        if 'user' in fruit:
            self.assertIsValidUser(fruit['user'])
            if user:
                self.assertIsSameUser(fruit['user'], user)
        if 'images' in fruit:
            self.assertIsValidUrl(fruit['images'], 'api:image-list', 'fruit', fruit['id'])

        self.assertTrue(isinstance(fruit['id'], int))
        self.assertTrue(fruit['kind'] in self.kind_keys)
        datetime.datetime.strptime(fruit['time'], '%Y-%m-%d %H:%M:%S')
        self.assertIsValidUrl(fruit['url'], 'api:fruit-detail', fruit['id'])


class TestFruitList(TestFruit):

    def test_list(self):
        response = self.client.get(self.fruit_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.fruit_list))
        self.assertItemsValid(response.data)

    def test_list_filtering(self):
        params = {
            'kind': self.kind_keys[1],
            'user': self.yuri.id,
        }
        response = self.client.get(self.fruit_list_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # should contain 1 item
        self.assertItemsValid(response.data)

    def test_list_pagination(self):
        params = {
            'limit': 2,
            'offset': 2,
        }
        response = self.client.get(self.fruit_list_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # should contain 2 items
        self.assertEqual(response.data['count'], len(self.fruit_list))
        self.assertIsNotNone(response.data['previous'])
        self.assertIsNone(response.data['next'])
        self.assertItemsValid(response.data['results'])

    def assertItemsValid(self, items):
        for item in items:
            self.assertIsValidFruit(item)


class TestFruitCreate(TestFruit):

    def test_create_not_authenticated(self):
        response = self.client.post(self.fruit_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_bad_data(self):
        self.login(self.yuri)

        data = self.fruit_data.copy()
        data['lat'] = '60.1234564567890'  # decimal too long
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.fruit_data.copy()
        data['kind'] = 'nonsense'  # non-existing type
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.fruit_data.copy()
        data['kind'] = 'nonsense'  # cannot change
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_data(self):
        self.login(self.yuri)

        data = self.fruit_data.copy()
        del(data['lat'])
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.fruit_data.copy()
        del(data['kind'])
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create(self):
        self.login(self.yuri)

        data = self.fruit_data.copy()
        data['description'] = 'test descriptión'
        response = self.client.post(self.fruit_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsValidFruit(response.data, self.yuri)
        self.assertEqual(response.data['description'], data['description'])


class TestFruitDetail(TestFruit):

    def test_retreive(self):
        response = self.client.get(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsValidFruit(response.data)

    def test_update_not_authenticated(self):
        response = self.client.put(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_bad_user(self):
        self.login(self.lara)

        response = self.client.put(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bad_data(self):
        self.login(self.yuri)

        data = {
            'lat': 'NaN',
        }
        response = self.client.patch(self.fruit_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.fruit_data.copy()
        del(data['lat'])  # field is required
        response = self.client.put(self.fruit_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        self.login(self.yuri)

        data = {
            'lat': Decimal('1'),
            'kind': self.kind_keys[1],
        }
        response = self.client.patch(self.fruit_url, data)  # modify data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['lat']), data['lat'])
        self.assertEqual(response.data['kind'], data['kind'])

        response = self.client.put(self.fruit_url, self.fruit_data)  # put data back
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsValidFruit(response.data, self.yuri)


class TestFruitDestroy(TestFruit):

    def test_destroy_not_authenticated(self):
        response = self.client.delete(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_bad_user(self):
        self.login(self.lara)

        response = self.client.delete(self.fruit_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        self.login(self.yuri)

        data = {
            'why_deleted': 'No fruit found'
        }
        response = self.client.delete(self.fruit_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.fruit_url)
        self.assertIsValidFruit(response.data, self.yuri)
        self.assertEqual(response.data['why_deleted'], data['why_deleted'])

        data = {
            'lat': '12.345',
        }
        response = self.client.patch(self.fruit_url, data)   # cannot update once deleted
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.fruit_url, data)  # cannot delete once deleted
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
