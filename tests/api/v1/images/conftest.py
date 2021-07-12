import base64
import os

import pytest
from django.conf import settings
from django.core.files.base import ContentFile

from fruit.models import Image

with open(os.path.join(settings.PROJECT_ROOT, "tests/data/small_image.jpg"), "rb") as image_file:
    SMALL_IMAGE_DATA_JPG = image_file.read()


with open(os.path.join(settings.PROJECT_ROOT, "tests/data/larger_image.jpg"), "rb") as image_file:
    LARGER_IMAGE_DATA_JPG = image_file.read()


@pytest.fixture
def small_image_jpg():
    return lambda: str(base64.b64encode(SMALL_IMAGE_DATA_JPG), encoding="ascii")


@pytest.fixture
def larger_image_jpg():
    return lambda: str(base64.b64encode(LARGER_IMAGE_DATA_JPG), encoding="ascii")


@pytest.fixture
def small_image_png():
    return lambda: "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="


@pytest.fixture
@pytest.mark.django_db
def new_image(small_image_jpg, new_user, random_string, new_fruit):
    def closure(**kwargs):
        image = kwargs.pop("image", None) or ContentFile(small_image_jpg(), name="image.jpg")
        author = kwargs.pop("author", None) or new_user()
        caption = kwargs.pop("caption", random_string(10))
        fruit = kwargs.pop("fruit", None) or new_fruit(user=author)

        return Image.objects.create(image=image, author=author, caption=caption, fruit=fruit, **kwargs)

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_images_list(small_image_jpg, new_user, random_string, new_fruit):
    def closure(length, **kwargs):
        image = kwargs.pop("image", None) or ContentFile(small_image_jpg(), name="image.jpg")
        author = kwargs.pop("author", None) or new_user()
        caption = kwargs.pop("caption", random_string(10))
        fruit = kwargs.pop("fruit", None) or new_fruit(user=author)

        return Image.objects.bulk_create(
            Image(image=image, author=author, caption=caption, fruit=fruit, **kwargs) for _ in range(length)
        )

    return closure


@pytest.fixture
def new_fruit_username_password(new_fruit, random_password, new_user):
    def closure():
        password = random_password()
        return new_fruit(), new_user(password=password).username, password

    return closure
