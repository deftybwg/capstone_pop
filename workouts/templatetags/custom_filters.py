from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, ["", "", ""])  # Default to empty values if key doesn't exist
