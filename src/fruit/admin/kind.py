from django import forms
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin


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
