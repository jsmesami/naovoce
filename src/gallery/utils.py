from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext, ugettext_lazy as _

from utils.tokenizer import Token
from .models import Image
from .forms import ImageUploadForm
from . import signals


def get_gallery_context(request, container):
    """
    Returns additional context for image-uploading views.
    """

    gallery_ct = ContentType.objects.get_for_model(container)
    token = str(Token(gallery_ct.id, container.id))
    public = container.is_gallery_public()

    if public and request.method == 'POST' and 'image_form' in request.POST:
        if request.user.is_authenticated():
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if request.POST.get('token') == token:
                    image = Image.objects.create(
                        image=form.cleaned_data.get('image'),
                        caption=form.cleaned_data.get('caption'),
                        author=request.user,
                        gallery_ct=gallery_ct,
                        gallery_id=container.id,
                    )
                    form = ImageUploadForm()
                    signals.image_created.send(
                        sender=Image,
                        image=image,
                        gallery_ct=gallery_ct,
                        gallery_id=container.id,
                    )
                    messages.success(request, ugettext('Thank you for adding an image.'))
                else:
                    form.add_error(None, _('Image not accepted.'))
        else:
            form = ImageUploadForm()
            messages.error(request, ugettext('You have to be signed-in to add images.'))
    else:
        form = ImageUploadForm() if public else None

    return {
        'image_form': form,
        'token': token,
        'images': Image.objects.filter(
            gallery_ct=gallery_ct,
            gallery_id=container.id,
        ).select_related('author'),
        'container': container,
    }
