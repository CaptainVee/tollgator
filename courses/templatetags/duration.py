from django import template

register = template.Library()


@register.filter
def minute_seconds(total_seconds):

    return ""
