from collections import OrderedDict
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


class FruitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = OrderedDict()
        for kind in Kind.objects.all():
            cls_name = Kind.CLS.text_of(kind.cls)
            groups.setdefault(cls_name, [])
            groups[cls_name].append((kind.pk, kind.name, kind.key))
        self.fields['kind'].choices = [('', _('Nothing selected'), 'F00D')] + [(cls, kind, '') for cls, kind in groups.items()]

    class Meta:
        model = Fruit
        fields = 'latitude', 'longitude', 'kind', 'description'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'kind': KindSelect(),
        }

    def clean_description(self):
        return self.cleaned_data['description'].strip()


class FruitDeleteForm(forms.Form):
    reason = forms.CharField(
        required=True,
        label=_('Reason'),
        help_text=_('Please describe reason of why you are deleting the marker.'),
        widget=forms.Textarea(attrs={'rows': 5}),
    )
