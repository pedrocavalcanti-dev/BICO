import unicodedata

from django import template

register = template.Library()


@register.filter
def get_field_errors(form, field_name):
    try:
        return form[field_name].errors
    except (KeyError, TypeError):
        return []


@register.filter
def category_icon(value):
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    icons = {
        "manut": "home",
        "jardin": "leaf",
        "pint": "paint",
        "eletr": "bolt",
        "encan": "drop",
        "limp": "sparkles",
        "mec": "tool",
        "tecno": "monitor",
        "inform": "monitor",
        "fotog": "camera",
        "design": "pen",
        "mont": "box",
        "reform": "home",
    }
    return next((icon for word, icon in icons.items() if word in value), "tool")


@register.filter
def specialty_groups(options):
    groups = {"Casa e manutenção": [], "Tecnologia e criação": [], "Outros serviços": []}
    for option in options:
        icon = category_icon(option.choice_label)
        if icon in {"monitor", "camera", "pen"}:
            group = "Tecnologia e criação"
        elif icon in {"leaf", "paint", "bolt", "drop", "sparkles", "box", "home"}:
            group = "Casa e manutenção"
        else:
            group = "Outros serviços"
        groups[group].append(option)
    return [{"label": label, "options": choices} for label, choices in groups.items() if choices]
