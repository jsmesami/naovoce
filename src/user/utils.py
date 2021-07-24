from django.db.models import Case, Count, When

from .models import FruitUser


def fruit_counter(**filters):
    return {"fruit_count": Count(Case(When(fruits__deleted=False, fruits__kind__deleted=False, then=1, **filters)))}


def top_users(**filters):
    return (
        FruitUser.objects.active()
        .filter(resolution=FruitUser.RESOLUTION.picker)
        .filter(**filters)
        .annotate(**fruit_counter(**filters))
        .order_by("-fruit_count", "username")
    )
