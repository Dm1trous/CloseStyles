from django import template

register = template.Library()


@register.filter(name='pluralize_товар')
def pluralize_товар(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return "товаров"

    last_digit = value % 10
    last_two_digits = value % 100

    if last_digit == 1 and last_two_digits != 11:
        return "товар"
    elif 2 <= last_digit <= 4 and (last_two_digits < 10 or last_two_digits >= 20):
        return "товара"
    else:
        return "товаров"


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ""


@register.filter
def filter_out_of_stock(cart_items):
    if not cart_items:
        return []
    return [item for item in cart_items if not item.product.statuss]

@register.filter
def filter_unavailable_items(cart_items):
    if not cart_items:
        return []
    return [item for item in cart_items if not item.product.statuss or not item.is_size_available]