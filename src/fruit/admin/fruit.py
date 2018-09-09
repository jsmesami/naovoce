from django.utils.translation import ugettext_noop, ugettext_lazy as _

from leaflet.admin import LeafletGeoAdmin

from .image import ImageAdminInline
from .comment import CommentAdminInline


class FruitAdmin(LeafletGeoAdmin):
    fields = 'position kind catalogue description user deleted why_deleted'.split()
    list_display = 'id __str__ user deleted _images_count _comments_count created'.split()
    list_filter = 'kind__name_cs deleted catalogue'.split()
    search_fields = 'id user__username user__email'.split()
    inlines = ImageAdminInline, CommentAdminInline

    def get_object(self, request, object_id, from_field=None):
        fruit = super().get_object(request, object_id)
        if fruit:
            fruit._was_deleted = fruit.deleted
        return fruit

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

        if not getattr(obj, '_was_deleted', False) and obj.deleted:
            # Inform user that we have deleted her marker.
            msg_template = ugettext_noop(
                'Site administrator deleted your <a href="{url}">marker</a>. '
                'Reason of deletion: {reason}'
            )
            context = dict(
                url=obj.frontend_url,
                reason=obj.why_deleted,
            )
            obj.user.send_message(msg_template, context=context, system=True)

    def _images_count(self, obj):
        return obj.images.count()
    _images_count.short_description = _('images')

    def _comments_count(self, obj):
        return obj.comments.count()
    _comments_count.short_description = _('comments')
