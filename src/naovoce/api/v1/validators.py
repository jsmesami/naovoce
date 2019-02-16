from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from utils import extension_for_mimetype


def validate_file_type(file, content_types):
    if file.content_type not in content_types:
        valid_extensions = ', '.join(map(extension_for_mimetype, content_types))
        raise ValidationError(_('Only {} files are allowed.'.format(valid_extensions)))


def validate_file_size(file, max_filesize):
    if file.size > max_filesize:
        max_megabytes = max_filesize / 1024 / 1024
        raise ValidationError(_('Uploaded file size exceeds {0:.2f} MB.'.format(max_megabytes)))
