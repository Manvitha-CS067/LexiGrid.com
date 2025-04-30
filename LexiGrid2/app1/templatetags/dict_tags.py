# app1/templatetags/dict_tags.py
from django import template

register = template.Library()

@register.filter
def get_dict_item(dictionary, key):
    """
    Access a dictionary value using a key.
    Example: {{ dictionary|get_dict_item:key }}
    """
    return dictionary.get(key)