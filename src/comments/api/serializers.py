from rest_framework import serializers

from ..models import Comment
from .. import signals


class CommentSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        super().save(**kwargs)

        signals.comment_created.send(
            sender=Comment,
            comment=self.instance,
            comment_type=self.instance.content_type,
            object_id=self.instance.object_id,
        )

    class Meta:
        model = Comment
        fields = 'text',
