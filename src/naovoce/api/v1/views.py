import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


@api_view()
def api_root(request, format=None):  # noqa:A002
    return Response(
        {
            "fruit": reverse("api:fruit-list", request=request, format=format),
            "herbarium": reverse("api:herbarium-list", request=request, format=format),
            "kinds": reverse("api:kinds-list", request=request, format=format),
            "users": reverse("api:users-list", request=request, format=format),
        }
    )


@api_view()
def api_handler_404(request, format=None):  # noqa:A002
    return Response(
        data=dict(detail=_("Not found.")),
        status=status.HTTP_404_NOT_FOUND,
    )


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:  # DRF couldn't handle the exception
        logger.exception("Uncaught Exception", exc_info=exc)
        return Response({"detail": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
