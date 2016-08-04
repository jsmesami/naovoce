from django.template import Library


register = Library()


@register.simple_tag
def choice_text(choices, index):
    return choices.text_of(index)


@register.simple_tag
def choice_name(choices, index):
    return choices.name_of(index)
