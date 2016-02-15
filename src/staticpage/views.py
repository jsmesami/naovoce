from django.shortcuts import get_object_or_404, render

from .models import StaticPage


def static_view(request, template_name=None):
    context = dict(staticpage=get_object_or_404(StaticPage, url=request.path))

    return render(request, template_name or 'staticpage/page.html', context)
