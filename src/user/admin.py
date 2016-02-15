from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import FruitUser


class FruitUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {
            'fields': 'username password'.split()
        }),
        (_('Personal info'), {
            'fields': [
                'first_name', 'last_name', ('email', 'is_email_verified')
            ],
        }),
        (_('Permissions'), {
            'fields': 'is_active is_staff is_superuser groups user_permissions'.split(),
        }),
        (_('Important dates'), {
            'fields': 'last_login date_joined'.split(),
        }),
    )

    list_display = 'username email first_name last_name is_staff is_active ' \
                   'is_email_verified date_joined'.split()

    list_filter = 'is_staff is_superuser is_active is_email_verified groups'.split()

    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['username email password1 password2'.split()]
        }),
    )


admin.site.register(FruitUser, FruitUserAdmin)
