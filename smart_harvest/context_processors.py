"""
Context processors for global template variables.
"""

from farmer.models import Alert


def alert_count(request):
    """Add unread alert count to all templates for the navbar badge."""
    if request.user.is_authenticated and hasattr(request.user, 'is_farmer') and request.user.is_farmer:
        count = Alert.objects.filter(user=request.user, is_read=False).count()
        return {'unread_alert_count': count}
    return {'unread_alert_count': 0}
