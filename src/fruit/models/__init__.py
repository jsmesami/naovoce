import random

from .fruit import Fruit
from .image import Image
from .kind import Kind


def _get_random_key():
    """
    Chooses random key from Yi syllables Unicode range.
    """
    return '{key:x}'.format(
        key=random.randint(0xA000, 0xA48C)
    )
