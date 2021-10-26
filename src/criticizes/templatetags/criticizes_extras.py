from django.template import Library

register = Library()

@register.filter
def model_type(value):
    return type(value).__name__

# pour afficher, dans les critiques, "vous" au lieu du pseudo de l'utilisateur connecté
@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context['user'] == user:
        return 'Vous avez'
    return f"{user.username} a"

# pour afficher, dans les tickets, "vous" au lieu du pseudo de l'utilisateur connecté
@register.simple_tag(takes_context=True)
def get_ticket_display(context, user):
    if context['user'] == user:
        return 'Vous avez publié ce ticket'
    return f"Ticket de {user.username}"
