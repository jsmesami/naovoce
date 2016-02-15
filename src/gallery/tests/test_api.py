import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.db import transaction
from rest_framework import status

from fruit.models import Fruit
from naovoce.tests import NaovoceAPITestCase
from gallery.models import Image


class TestImage(NaovoceAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        gallery_ct = ContentType.objects.get_for_model(Fruit)
        gallery_id = cls.fruit.id

        cls.image_data = {
            'gallery_ct': gallery_ct,
            'gallery_id': gallery_id,
            'image': cls.get_image_file(),
        }
        # create some images (5 by Yuri + 3 by Lara)
        with transaction.atomic():
            cls.image_list = [
                Image.objects.create(
                    author=getattr(cls, author),
                    **cls.image_data
                )
                for author in ('yuri '*5).split() + ('lara '*3).split()
            ]

        cls.image = cls.image_list[0]

        cls.image_list_url = reverse('api:image-list', args=[gallery_ct.model, gallery_id])
        cls.image_url = reverse('api:image-detail', args=[cls.image.pk])

    @staticmethod
    def get_image_file():
        image_path = os.path.join(settings.STATIC_ROOT, 'img/holder_01.png')
        return SimpleUploadedFile(
            name='test_image.png',
            content=open(image_path, 'rb').read(),
            content_type='image/png',
        )

    def assertIsValidImage(self, image, user=None):
        self.assertTrue(isinstance(image['id'], int))
        self.assertTrue(isinstance(image['image'], str))
        self.assertTrue(image['image'])
        self.assertTrue(isinstance(image['caption'], str))
        self.assertIsValidUser(image['author'])
        if user:
            self.assertIsSameUser(image['author'], user)


class TestImageList(TestImage):

    def test_list(self):
        response = self.client.get(self.image_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.image_list))
        self.assertItemsValid(response.data)

    def test_list_pagination(self):
        params = {
            'limit': 4,
            'offset': 0,
        }
        response = self.client.get(self.image_list_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['count'], len(self.image_list))
        self.assertIsNone(response.data['previous'])
        self.assertIsNotNone(response.data['next'])
        self.assertItemsValid(response.data['results'])

        params = {
            'limit': 4,
            'offset': 4,
        }
        response = self.client.get(self.image_list_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['count'], len(self.image_list))
        self.assertIsNotNone(response.data['previous'])
        self.assertIsNone(response.data['next'])
        self.assertItemsValid(response.data['results'])

    def assertItemsValid(self, items):
        for item in items:
            self.assertIsValidImage(item)


class TestImageCreate(TestImage):

    def test_create_not_authenticated(self):
        response = self.client.post(self.image_list_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_bad_data(self):
        self.login(self.yuri)

        data = self.image_data.copy()
        data['image'] = 'nonsense'
        response = self.client.post(self.image_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_data(self):
        self.login(self.yuri)

        data = self.image_data.copy()
        del(data['image'])
        response = self.client.post(self.image_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create(self):
        self.login(self.yuri)

        data = self.image_data.copy()
        data['image'] = self.get_image_file()
        data['caption'] = 'test captión'
        response = self.client.post(self.image_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsValidImage(response.data, self.yuri)
        self.assertEqual(response.data['caption'], data['caption'])


class TestImageDetail(TestImage):

    def test_retreive(self):
        response = self.client.get(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsValidImage(response.data)

    def test_update_not_authenticated(self):
        response = self.client.put(self.image_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(self.image_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bad_user(self):
        self.login(self.lara)

        response = self.client.put(self.image_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bad_data(self):
        self.login(self.yuri)

        data = {
            'image': 'nonsense',
        }
        response = self.client.patch(self.image_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.image_data.copy()
        data['image'] = None
        response = self.client.put(self.image_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        self.login(self.yuri)

        orig_image = self.client.get(self.image_url).data['image']
        data = {
            'image': self.get_image_file(),
            'caption': 'captión',
        }
        response = self.client.patch(self.image_url, data)
        self.assertIsValidImage(response.data, self.yuri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['caption'], data['caption'])
        self.assertNotEqual(response.data['image'], orig_image)


class TestImageDestroy(TestImage):

    def test_destroy_not_authenticated(self):
        response = self.client.delete(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_bad_user(self):
        self.login(self.lara)

        response = self.client.delete(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        self.login(self.yuri)

        response = self.client.delete(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
