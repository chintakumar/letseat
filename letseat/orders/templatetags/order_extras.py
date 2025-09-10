from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def calc_total(order_items):
    total = 0
    for item in order_items:
        total += item.food_item.price * item.quantity
    return total
