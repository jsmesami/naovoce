from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Image


class ImageUploadForm(forms.ModelForm):
    tamper = forms.CharField(
        required=False,
        label='If you are not human, please fill this',
        max_length=255,
        widget=forms.Textarea(),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Tampered honeypot must raise non-field error, because it's hidden by css.
        tamper = self.cleaned_data.get('tamper')
        if tamper != '':
            raise forms.ValidationError(_('Image not accepted.'))

        return cleaned_data

    class Meta:
        model = Image
        fields = 'image caption tamper'.split()


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
