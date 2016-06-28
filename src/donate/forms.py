import django.forms

class DonateForm(django.forms.Form):
    amount = django.forms.DecimalField()
