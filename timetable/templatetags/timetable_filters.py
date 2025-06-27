from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def items(dictionary):
    if dictionary is None:
        return []
    return dictionary.items() 