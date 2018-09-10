import datetime

from django.db.models import Case, Count, When
from fruit.models import Fruit

from .models import FruitUser


def fruit_counter(**filters):
    return {
        'fruit_count': Count(Case(When(fruits__deleted=False, then=1, **filters)))
    }


def top_pickers(**filters):
    return FruitUser.objects.active()\
        .filter(resolution=FruitUser.RESOLUTION.picker)\
        .filter(**filters)\
        .annotate(**fruit_counter(**filters))\
        .order_by('-fruit_count', 'username')


def pickers_counts_context():
    top_all_time = top_pickers()

    last_month = datetime.date.today() - datetime.timedelta(365 / 12)
    top_last_month = top_pickers(fruits__created__gte=last_month).exclude(fruit_count=0)

    return dict(
        top_pickers_all_time=top_all_time[:10],
        top_pickers_last_month=top_last_month[:4],
        pickers_count=FruitUser.objects.active().order_by().count(),
        fruit_count=Fruit.objects.valid().order_by().count(),
    )
