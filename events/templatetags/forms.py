from django import template

register = template.Library()

@register.filter
def bulma_message_tag(tag):
    """
    messages use type "error", while bulma use class "danger"
    """
    return {
        'error': 'danger'
    }.get(tag, tag)
