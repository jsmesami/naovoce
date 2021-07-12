from operator import itemgetter

from rest_framework.fields import DateTimeField
from rest_framework.reverse import reverse

HTTP_METHODS = {"get", "post", "put", "delete", "options", "trace", "patch"}


def render_view_url(response, viewname, *args):
    return reverse(viewname, args=args, request=response.renderer_context["request"])


def get_full_url(response, url):
    server = response.renderer_context["request"].META["SERVER_NAME"]
    return f"http://{server}{url}"


def format_coord(coord):
    return f"{coord:.10f}"


def format_time(time):
    return DateTimeField(format="%Y-%m-%d %H:%M:%S").to_representation(time)


def sort_by_key(key, coll):
    return sorted(coll, key=itemgetter(key))
