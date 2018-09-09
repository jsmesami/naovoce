from django.contrib import admin

from fruit.herbarium.models import Herbarium
from fruit.models import Comment, Image, Kind, Fruit

from .comment import CommentAdmin
from .fruit import FruitAdmin
from .herbarium import HerbariumAdmin
from .image import ImageAdmin
from .kind import KindAdmin

admin.site.register(Comment, CommentAdmin)
admin.site.register(Herbarium, HerbariumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Fruit, FruitAdmin)
