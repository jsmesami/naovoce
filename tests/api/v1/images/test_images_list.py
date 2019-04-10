from functools import partial
from rest_framework import status
from rest_framework.reverse import reverse

from . import image_to_data
from ..utils import sort_by_key


def test_images_list(client, new_fruit_list, new_images_list):
    length = 2
    fruit1, fruit2, fruit3 = new_fruit_list(3)
    images1 = new_images_list(length, fruit=fruit1)
    images2 = new_images_list(length, fruit=fruit2)

    response = client.get(reverse('api:image-list', args=[fruit1.id]))

    expected = map(partial(image_to_data, response=response), images1)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == length
    assert sort_by_key('id', response.json()) == sort_by_key('id', expected)

    response = client.get(reverse('api:image-list', args=[fruit2.id]))

    expected = map(partial(image_to_data, response=response), images2)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == length
    assert sort_by_key('id', response.json()) == sort_by_key('id', expected)

    response = client.get(reverse('api:image-list', args=[fruit3.id]))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
