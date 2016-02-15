from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.core.urlresolvers import reverse

from blog.models import BlogPost
from fruit.models import Fruit
from fruit.herbarium.models import Herbarium
from user.models import FruitUser
from staticpage.models import StaticPage


__all__ = ['sitemaps']


class IndexesSitemap(Sitemap):
    indexes = {
        'home': {
            'priority': 0.7,
            'changefreq': 'hourly',
        },
        'herbarium:index': {
            'priority': 0.8,
            'changefreq': 'monthly',
        },
        'blog:index': {
            'priority': 0.9,
            'changefreq': 'weekly',
        },
        'pickers:index': {
            'priority': 0.3,
            'changefreq': 'weekly',
        },
    }

    def items(self):
        return list(self.indexes.keys())

    def location(self, item):
        return reverse(item)

    def changefreq(self, item):
        return self.indexes[item]['changefreq']

    def priority(self, item):
        return self.indexes[item]['priority']


sitemaps = {
    'indexes': IndexesSitemap(),
    'blogs': GenericSitemap(dict(
        queryset=BlogPost.objects.public()),
        priority=1,
        changefreq='yearly',
    ),
    'herbarium': GenericSitemap(dict(
        queryset=Herbarium.objects.all()),
        priority=0.6,
        changefreq='yearly',
    ),
    'staticpages': GenericSitemap(dict(
        queryset=StaticPage.objects.all()),
        priority=0.5,
        changefreq='monthly',
    ),
    'pickers': GenericSitemap(dict(
        queryset=FruitUser.objects.filter(is_active=True)),
        priority=0.4,
        changefreq='weekly',
    ),
    'fruit': GenericSitemap(dict(
        queryset=Fruit.objects.order_by('-created')[:10000]),
        priority=0.2,
        changefreq='yearly',
    ),
}
