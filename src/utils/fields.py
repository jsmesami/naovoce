from django.db import models
from django.forms import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from sorl.thumbnail import ImageField


class AutoDateTimeField(models.DateTimeField):
    """
    A field that saves timezone-aware datetime on each save.
    """
    def pre_save(self, model_instance, add):
        return timezone.now()


class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop("max_upload_size", [])

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        if file and hasattr(file, 'content_type'):
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))

        return data


class ContentTypeRestrictedImageField(ContentTypeRestrictedFileField, ImageField):
    # just mixing these two together
    pass
