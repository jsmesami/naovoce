from django.contrib import admin
from django import forms

from .models import StaticPage


class AdminForm(forms.ModelForm):
    meta_description = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 86, 'maxlength': 150}), required=False)

    class Meta:
        model = StaticPage
        fields = '__all__'


class StaticPageAdmin(admin.ModelAdmin):
    fields = 'url title text meta_description'.split()
    list_display = 'url title'.split()

    form = AdminForm


admin.site.register(StaticPage, StaticPageAdmin)
