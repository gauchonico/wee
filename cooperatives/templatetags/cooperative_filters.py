from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using the key"""
    return dictionary.get(key)

@register.filter
def sum_quantity(collections):
    """Sum the quantities of a list of collections"""
    return sum(collection.quantity for collection in collections) 