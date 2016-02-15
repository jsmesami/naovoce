from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'text', 'content_type', 'object_id',
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()

        if text == '':
            raise forms.ValidationError(_('Comment cannot be empty.'))

        return text
