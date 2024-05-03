from django import template
from django.utils.text import slugify
from django.utils import timezone
from Appsocialmedia.models import *

register = template.Library()

@register.filter(name='date_calc')
def date_calc(data, arg):
    date_difference = timezone.now() - arg
    total_seconds = abs(date_difference.total_seconds())

    if total_seconds < 60:
        return f"{int(total_seconds)} saniye önce"
    elif total_seconds < 3600:
        return f"{int(total_seconds / 60)} dakika önce"
    elif total_seconds < 86400:
        return f"{int(total_seconds / 3600)} saat önce"
    else:
        return f"{int(total_seconds / 86400)} gün önce"