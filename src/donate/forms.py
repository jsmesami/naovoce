import django.forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

MIN_DONATION_VALUE = 200

class DonateForm(django.forms.Form):
    amount = django.forms.DecimalField(initial=MIN_DONATION_VALUE,
                                       validators=[MinValueValidator(MIN_DONATION_VALUE,
                                                                     message=_('We accept only donations higher than {0} CZK').format(MIN_DONATION_VALUE))])
