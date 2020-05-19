# coding=utf-8
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name='human_format')
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


# @register.filter
# def highlight_search(text, search):
#     pattern = re.compile(re.escape(search), re.IGNORECASE)
#     highlighted = pattern.sub('<mark>\g<0></mark>', text)
#     return mark_safe(highlighted)


import re
@register.filter
def highlight(value, search_term, autoescape=True):
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    new_value = pattern.sub('<mark>\g<0></mark>', value)
    return mark_safe(new_value)

