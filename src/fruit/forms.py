from collections import OrderedDict
from itertools import chain
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import Fruit, Kind


class KindSelect(forms.Select):
    """
    This is here to render data-key="Fruit.key" attribute to <select> options
    later used by form's javascript
    """
    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []

        for option_value, option_label, option_key in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label, option_key))

        return '\n'.join(output)

    def render_option(self, *args):
        selected_choices, option_value, option_label, option_key = args
        option_value = force_text(option_value)

        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            selected_choices.remove(option_value)
        else:
            selected_html = ''

        return format_html('<option value="{}"{} data-key="{}">{}</option>',
                           option_value,
                           selected_html,
                           option_key,
                           force_text(option_label))


class CatalogueWidget(CheckboxInput):
    def __init__(self):
        super().__init__(check_test=lambda val: val == Fruit.CATALOGUE.revival)

    def value_from_datadict(self, data, *args):
        return Fruit.CATALOGUE.revival if data.get('catalogue') else Fruit.CATALOGUE.naovoce


class FruitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = OrderedDict()
        for kind in Kind.objects.all():
            cls_name = Kind.CLS.text_of(kind.cls)
            groups.setdefault(cls_name, [])
            groups[cls_name].append((kind.pk, kind.name, kind.key))
        self.fields['kind'].choices = [
            ('', _('Nothing selected'), 'F00D')
        ] + [(cls, kind, '') for cls, kind in groups.items()]

    class Meta:
        model = Fruit
        fields = 'latitude', 'longitude', 'kind', 'description', 'catalogue'

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'latitude': forms.NumberInput(attrs={'min': -90, 'max': 90}),
            'longitude': forms.NumberInput(attrs={'min': -180, 'max': 180}),
            'kind': KindSelect(),
            'catalogue': CatalogueWidget(),
        }

        labels = {
            'catalogue': _('Is it a tree that you planted yourself?')
        }

    def clean_latitude(self):
        lat = self.cleaned_data['latitude']
        if -90 <= lat <= 90:
            return lat
        else:
            raise ValidationError(_('Latitude must be a number between -90 and 90.'))

    def clean_longitude(self):
        lng = self.cleaned_data['longitude']
        if -180 <= lng <= 180:
            return lng
        else:
            raise ValidationError(_('Longitude must be a number between -180 and 180.'))

    def clean_description(self):
        return self.cleaned_data['description'].strip()


class FruitDeleteForm(forms.Form):
    reason = forms.CharField(
        required=True,
        label=_('Reason'),
        help_text=_('Please describe reason of why you are deleting the marker.'),
        widget=forms.Textarea(attrs={'rows': 5}),
    )
