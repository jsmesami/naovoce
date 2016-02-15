from django.shortcuts import render


def plain_text_view(request, template_name):
    return render(request, template_name, content_type='text/plain')
