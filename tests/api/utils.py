from rest_framework.reverse import reverse


def render_url(response, viewname, *args):
    return reverse(viewname, args=args, request=response.renderer_context['request'])
