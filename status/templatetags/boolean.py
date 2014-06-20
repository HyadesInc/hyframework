from django import template

register = template.Library()

@register.filter(name="not_value")
def not_value(true_value):
    return not true_value