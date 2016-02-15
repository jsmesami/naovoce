from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from gallery.managers import GalleryManager
from gallery.models import GalleryModel
from utils.models import TimeStampedModel


class Category(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    @property
    def slug(self):
        return slugify(self.name)

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.id, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class PublicBlogPostQuerySet(models.QuerySet):
    def public(self):
        return self.filter(public_from__lte=timezone.now())


class BlogPost(TimeStampedModel, GalleryModel):
    title = models.CharField(_('title'), max_length=255)
    text = models.TextField(_('text'))

    categories = models.ManyToManyField(
        Category,
        verbose_name=_('categories'),
        related_name='blogposts',
    )
    public_from = models.DateTimeField(
        _('public from'),
        default=timezone.now,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        editable=False,
    )

    objects = GalleryManager.from_queryset(PublicBlogPostQuerySet)()

    @cached_property
    def slug(self):
        return slugify(self.title)

    @property
    def is_public(self):
        return self.public_from <= timezone.now()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = '-public_from', '-created'
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
