from django import forms

from .models import Image


class CoverImageAdminForm(forms.ModelForm):
    """
    Use ``form = CoverImageAdminForm`` in your admin class to limit cover_image choices
    to images related to the instance
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_image'].queryset = Image.objects.filter(
            gallery_id=self.instance.pk
        )
