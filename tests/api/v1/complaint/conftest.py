from datetime import date

import pytest
from django.utils.formats import date_format
from django.utils.html import format_html

from fruit.models.comment import COMPLAINT_MSG


@pytest.fixture
def complaint_text():
    def closure(fruit):
        text = format_html(
            COMPLAINT_MSG,
            user_url=fruit.user.get_absolute_url(),
            user_name=fruit.user.username,
            fruit_url=fruit.get_absolute_url(),
        )
        return format_html(
            "<span class='date'>{date}</span> {text}",
            date=date_format(date.today(), "SHORT_DATE_FORMAT", use_l10n=True),
            text=text,
        )

    return closure
