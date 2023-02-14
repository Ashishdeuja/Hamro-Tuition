from django import template

register = template.Library()

@register.filter(name='split_first')
def split_first(value):
    return value[0]