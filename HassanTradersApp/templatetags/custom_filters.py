from django import template

register = template.Library()


@register.filter
def split_url(value, arg):
    return value.split(arg)
