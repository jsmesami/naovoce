from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_noop, ugettext_lazy as _
from django import forms

from leaflet.admin import LeafletGeoAdmin

from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from gallery.admin import ImageAdminInline, GalleryAdminMixin
from gallery.forms import CoverImageAdminForm
from .models import Kind, Fruit
from .herbarium.models import Herbarium, Season


class KindModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['key'] = self.instance.strkey


class KindAdmin(TranslationAdmin):
    fields = 'cls name color key deleted'.split()
    list_display = 'name _class _color _fruit_count key deleted'.split()

    def _class(self, obj):
        return obj.CLS.text_of(obj.cls)
    _class.short_description = _('class')
    _class.admin_order_field = 'cls'

    def _color(self, obj):
        color_html = '<div class="cbox" style="background:#{color}"></div> #{color}'
        return format_html(color_html, color=obj.color)
    _color.short_description = _('color')
    _color.allow_tags = True

    def _fruit_count(self, obj):
        return obj.fruits.count()
    _fruit_count.short_description = _('markers count')

    def has_delete_permission(self, request, obj=None):
        return False


class FruitAdmin(GalleryAdminMixin, LeafletGeoAdmin):
    fields = 'position kind catalogue description user deleted why_deleted cover_image'.split()
    list_display = 'id __str__ _position user _deleted images_count created'.split()
    list_filter = 'kind__name_cs catalogue'.split()
    search_fields = 'id user__username user__email'.split()
    form = CoverImageAdminForm
    inlines = ImageAdminInline,

    def _position(self, obj):
        return '{}, {}'.format(obj.position.x, obj.position.y)
    _position.short_description = _('position')

    def _deleted(self, obj):
        return obj.is_deleted
    _deleted.short_description = _('deleted')
    _deleted.boolean = True

    def get_object(self, request, object_id, from_field=None):
        fruit = super().get_object(request, object_id)
        if fruit:
            fruit._was_deleted = fruit.is_deleted
        return fruit

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

        if not getattr(obj, '_was_deleted', False) and obj.is_deleted:
            # Inform user that we have deleted her marker.
            msg_template = ugettext_noop(
                'Site administrator deleted your <a href="{url}">marker</a>. '
                'Reason of deletion: {reason}'
            )
            context = dict(
                url=obj.get_absolute_url(),
                reason=obj.why_deleted,
            )
            obj.user.send_message(msg_template, context=context, system=True)


class SeasonAdminInline(TranslationTabularInline):
    model = Season
    allow_add = True
    extra = 0


class HerbariumAdmin(admin.ModelAdmin):
    model = Herbarium
    list_display = 'kind full_name latin_name'.split()
    inlines = SeasonAdminInline,


admin.site.register(Herbarium, HerbariumAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Fruit, FruitAdmin)
