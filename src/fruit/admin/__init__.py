from django.contrib import admin

from fruit.models import Comment, Fruit, Image, Kind

from .comment import CommentAdmin
from .fruit import FruitAdmin
from .image import ImageAdmin
from .kind import KindAdmin

admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Fruit, FruitAdmin)
