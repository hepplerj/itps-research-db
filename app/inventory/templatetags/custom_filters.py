from django import template

register = template.Library()


@register.filter
def format_date_range(value):
    if value:
        return f"{value.lower} - {value.upper}"
    return ""
