from django.dispatch import Signal

comment_created = Signal(providing_args=['comment', 'comment_type', 'object_id'])
