from collections import OrderedDict
from django import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput
from django.utils.translation import ugettext_lazy as _

from .models import Fruit, Kind


class CatalogueWidget(CheckboxInput):
    template_name = 'fruit/checkbox.html'  # Hotfix: widget gets otherwise rendered as required for unknown reason.

    def __init__(self):
        super().__init__(check_test=lambda val: val == Fruit.CATALOGUE.revival)

    def value_from_datadict(self, data, *args):
        return Fruit.CATALOGUE.revival if data.get('catalogue') else Fruit.CATALOGUE.naovoce


class FruitForm(forms.ModelForm):
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = OrderedDict()
        for kind in Kind.objects.valid():
            cls_name = Kind.CLS.text_of(kind.cls)
            groups.setdefault(cls_name, [])
            groups[cls_name].append((kind.pk, kind.name))
        self.fields['kind'].choices = [
            ('', [(_('Nothing selected'), 'F00D')])
        ] + [(cls, kind) for cls, kind in groups.items()]

    class Meta:
        model = Fruit
        fields = 'latitude', 'longitude', 'position', 'kind', 'description', 'catalogue'

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'latitude': forms.NumberInput(attrs={'min': -90, 'max': 90}),
            'longitude': forms.NumberInput(attrs={'min': -180, 'max': 180}),
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

    def clean(self):
        data = super().clean()
        data['position'] = Point(float(data.pop('longitude')), float(data.pop('latitude')))
        return data


class FruitDeleteForm(forms.Form):
    reason = forms.CharField(
        required=True,
        label=_('Reason'),
        help_text=_('Please describe reason of why you are deleting the marker.'),
        widget=forms.Textarea(attrs={'rows': 5}),
    )
