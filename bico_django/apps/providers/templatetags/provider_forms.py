from django import template

register = template.Library()


@register.filter
def get_field_errors(form, field_name):
    try:
        return form[field_name].errors
    except (KeyError, TypeError):
        return []
