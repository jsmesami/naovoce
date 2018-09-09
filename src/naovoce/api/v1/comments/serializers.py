from rest_framework import serializers

from fruit.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        super().save(**kwargs)

    class Meta:
        model = Comment
        fields = 'text',
