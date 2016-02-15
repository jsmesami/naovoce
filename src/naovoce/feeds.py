import django.contrib.syndication.views as syndication
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from blog.models import BlogPost
from fruit.models import Fruit


class BlogFeed(syndication.Feed):
    title = 'Na-ovoce.cz'
    description = 'Blog'
    description_template = 'feeds/blog.html'

    def link(self):
        return reverse('rss-blog')

    def items(self):
        return BlogPost.objects.public().select_related('author')[:5]

    def item_author_name(self, obj):
        return obj.author.get_short_name()

    def item_author_email(self, obj):
        return obj.author.email

    def item_description(self, obj):
        return obj.title

    def item_pubdate(self, obj):
        return obj.public_from


class FruitFeed(syndication.Feed):
    title = 'Na-ovoce.cz'
    description = _('Fresh fruit')

    def link(self):
        return reverse('rss-fruit')

    def items(self):
        return Fruit.objects.select_related('user').order_by('-created')[:30]

    def item_author_name(self, obj):
        return obj.user.get_short_name()

    def item_description(self, obj):
        return obj.description

    def item_pubdate(self, obj):
        return obj.created
