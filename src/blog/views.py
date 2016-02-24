from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render

from comments.utils import get_comments_context
from .models import BlogPost, Category


def index(request, category_pk=None, category_slug=None):
    if category_pk:
        cat = get_object_or_404(Category, pk=category_pk)
        if cat.slug != category_slug:
            return HttpResponsePermanentRedirect(cat.get_absolute_url())
        blogposts = BlogPost.objects.public().filter(categories=cat)
    else:
        blogposts = BlogPost.objects.public()

    template_name = 'blog/page.html' if request.is_ajax() else 'blog/index.html'

    context = {
        'categories': Category.objects.filter(blogposts__isnull=False).distinct(),
        'category_pk': int(category_pk or 0),
        'blogposts': blogposts,
    }
    return render(request, template_name, context)


def detail(request, pk, slug=None):
    qs = BlogPost.objects.public().filter(id=pk)
    entry = get_object_or_404(qs)

    if entry.slug != slug:
        return HttpResponsePermanentRedirect(entry.get_absolute_url())

    context = {'entry': entry}
    context.update(get_comments_context(request, container=entry))
    return render(request, 'blog/detail.html', context)
