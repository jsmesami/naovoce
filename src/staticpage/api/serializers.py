from rest_framework import serializers

from utils.api.fields import MarkdownField
from ..models import StaticPage


class PageRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = 'url', 'title', 'text', 'meta_description'


class PageSerializer(PageRawSerializer):
    text = MarkdownField()
