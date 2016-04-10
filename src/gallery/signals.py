from django.dispatch import Signal

image_created = Signal(providing_args=['image', 'gallery_ct', 'gallery_id'])
image_removed = Signal(providing_args=['image', 'gallery_ct', 'gallery_id'])
