from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    tamper = forms.CharField(
        required=False,
        label='If you are not human, please fill this',
        max_length=255,
        widget=forms.Textarea(),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Tampered honeypot must raise non-field error, because it's hidden by css.
        tamper = self.cleaned_data.get('tamper')
        if tamper != '':
            raise forms.ValidationError(_('Comment not accepted.'))

        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if text == '':
            raise forms.ValidationError(_('You do not want to post empty comment, do you?'))

        return text

    class Meta:
        model = Comment
        fields = 'text', 'tamper'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


def comment_form_factory(with_complaints=False, complaint_label=None):
    if not with_complaints:
        return CommentForm
    else:
        return type(
            'ComplaintForm',
            (CommentForm,),
            dict(
                complaint=forms.BooleanField(
                    required=False,
                    label=complaint_label,
                ),
                base_fields='text complaint tamper'.split()
            )
        )
