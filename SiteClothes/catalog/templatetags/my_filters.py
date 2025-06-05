from django import template

register = template.Library()

@register.filter(name='pluralize_товар')
def pluralize_товар(value):
    value = int(value)
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
    return value * arg

