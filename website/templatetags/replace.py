from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    return value.replace("%s", arg)
