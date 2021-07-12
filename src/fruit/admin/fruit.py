from django.utils.translation import ugettext_lazy as _, ugettext_noop
from leaflet.admin import LeafletGeoAdmin

from .comment import CommentAdminInline
from .image import ImageAdminInline


class FruitAdmin(LeafletGeoAdmin):
    fields = "position kind catalogue description user deleted why_deleted".split()
    list_display = "id __str__ _position user _deleted _images_count _comments_count created".split()
    list_filter = "kind__name_cs catalogue".split()
    search_fields = "id user__username user__email".split()
    inlines = ImageAdminInline, CommentAdminInline

    def get_object(self, request, object_id, from_field=None):
        fruit = super().get_object(request, object_id)
        if fruit:
            fruit._was_deleted = fruit.is_deleted
        return fruit

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

        if not getattr(obj, "_was_deleted", False) and obj.is_deleted:
            # Inform user that we have deleted her marker.
            msg_template = ugettext_noop(
                'Site administrator deleted your <a href="{url}">marker</a>. ' "Reason of deletion: {reason}"
            )
            context = dict(
                url=obj.frontend_url,
                reason=obj.why_deleted,
            )
            obj.user.send_message(msg_template, context=context, system=True)

    def _position(self, obj):
        return f"{obj.position.x}, {obj.position.y}"

    _position.short_description = _("position")

    def _deleted(self, obj):
        return obj.is_deleted

    _deleted.short_description = _("deleted")
    _deleted.boolean = True

    def _images_count(self, obj):
        return obj.images.count()

    _images_count.short_description = _("images")

    def _comments_count(self, obj):
        return obj.comments.count()

    _comments_count.short_description = _("comments")

    def has_delete_permission(self, request, obj=None):
        return False
