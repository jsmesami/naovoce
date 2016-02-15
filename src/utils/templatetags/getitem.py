from django.template import Library


register = Library()


@register.filter
def getitem(dictionary, k):
    return dictionary.get(k)
