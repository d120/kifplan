from django import template

register = template.Library()


@register.filter
def vis_bool(value):
    if value:
        return "&#x2714; Ja"
    return "x Nein"
