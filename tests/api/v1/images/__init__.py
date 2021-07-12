from fruit.models import Image

from ..users import user_to_data
from ..utils import get_full_url

CAPTION_MAX_LENGTH = Image._meta.get_field("caption").max_length

CREATE_IMAGE_BAD_ARGS = [
    (
        {"caption": "c" * (CAPTION_MAX_LENGTH + 1)},
        {"caption": [f"Ensure this field has no more than {CAPTION_MAX_LENGTH} characters."]},
    ),
    ({"caption": None}, {"caption": ["This field may not be null."]}),
    ({"image": None}, {"image": ["This field may not be null."]}),
    (
        {"image": "rubbish"},
        {"image": ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."]},
    ),
]


def image_to_data(image, response):
    return {
        "id": image.id,
        "image": get_full_url(response, image.image.url),
        "caption": image.caption,
        "author": user_to_data(image.author, response),
    }
