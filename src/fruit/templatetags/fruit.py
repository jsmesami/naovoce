from django.template import Library

register = Library()


@register.filter
def can_edit(user, fruit):
    return user.is_authenticated() and fruit.user_id == user.id and not fruit.deleted
