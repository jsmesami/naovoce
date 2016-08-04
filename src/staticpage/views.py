from django.shortcuts import get_object_or_404, render

from .models import StaticPage


def static_view(request, template_name=None, additional_context=None):
    context = dict(staticpage=get_object_or_404(StaticPage, url=request.path))
    if additional_context:
        context.update(additional_context)

    return render(request, template_name or 'staticpage/page.html', context)
