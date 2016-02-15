from itertools import chain
from django import forms
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

        for option_key, option_value, option_label in chain(self.choices, choices):
            output.append(self.render_option(selected_choices,
                                             option_value, option_label, option_key))

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


class FruitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        kinds = Kind.objects.values_list('key', 'pk', 'name')
        self.fields['kind'].choices = [('F00D', '', _('Nothing selected'))] + list(kinds)

    class Meta:
        model = Fruit
        fields = 'latitude', 'longitude', 'kind', 'description'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'kind': KindSelect(),
        }

    def clean_description(self):
        return self.cleaned_data['description'].strip()
