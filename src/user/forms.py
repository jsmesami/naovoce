from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import FruitUser, Message


class UserCreationForm(forms.ModelForm):
    username = forms.RegexField(
        label=_('username'),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. "
                    "Letters, digits and @/./+/-/_ only."),
        error_messages={'invalid': _("This value may contain only letters, "
                                     "numbers and @/./+/-/_ characters.")},
    )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = FruitUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_('username'),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_('Required. 30 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        error_messages={'invalid': _('This value may contain only letters, '
                                     'numbers and @/./+/-/_ characters.')},
    )
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_('Raw passwords are not stored, so there is no way to see '
                    'this user\'s password, but you can change the password '
                    'using <a href="password/">this form</a>.'),
    )

    class Meta:
        model = FruitUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 86, 'maxlength': 255}),
        }
