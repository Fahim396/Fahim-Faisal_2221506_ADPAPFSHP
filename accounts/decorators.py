"""
Role-based access decorators for view protection.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """Restrict view access to specific roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect('accounts:login')
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def farmer_required(view_func):
    """Restrict access to farmers only."""
    return role_required(['farmer'])(view_func)


def admin_required(view_func):
    """Restrict access to admins only."""
    return role_required(['admin'])(view_func)
