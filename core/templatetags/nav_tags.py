from django import template

register = template.Library()


@register.simple_tag
def get_section_name(path):
    """Extract section name from URL path"""

    clean_path = path.strip("/")
    if not clean_path:
        return "Dashboard"

    section = clean_path.split("/")[0]
    return section.title() if section else "Dashboard"
