from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import List, Campaign, Asset, ClientError


class ListAdmin(admin.ModelAdmin):
    list_display = 'name', 'hash'


class AssetAdminInline(admin.TabularInline):
    model = Asset
    allow_add = True
    extra = 0

    def file_url(self, obj):
        return obj.file.url
    file_url.short_description = 'url'

    readonly_fields = 'file_url',


class CampaignAdmin(admin.ModelAdmin):
    search_fields = 'subject',
    list_display = 'subject assets_count sent'.split()
    list_filter = 'sent',
    inlines = AssetAdminInline,

    def assets_count(self, obj):
        return obj.assets.count()
    assets_count.short_description = _('assets')

    def save_model(self, request, obj, form, change):
        obj.save()
        if request.POST.get('save_and_send'):
            try:
                obj.create_draft()
                obj.sent = True
                obj.save()
                messages.info(request, _('Campaign has been sent to the mailing list.'))
            except ClientError as e:
                messages.error(request, '{} ({}).'.format(_('Campaign has not been sent to the mailing list'), e))


admin.site.register(List, ListAdmin)
admin.site.register(Campaign, CampaignAdmin)
