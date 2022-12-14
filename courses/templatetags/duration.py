from django import template
from datetime import time

register = template.Library()


@register.filter
def hour_minute(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}hr {minutes}min"
    return f"{minutes}min"


@register.filter
def hour(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours < 10:
        return f"0{hours}hr"
    return f"{hours}hr"


@register.filter
def hour_minute_second(formated_time):
    if formated_time[:2] != "00":
        return formated_time
    return formated_time[3:]
