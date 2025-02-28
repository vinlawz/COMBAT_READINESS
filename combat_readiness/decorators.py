from django.core.exceptions import PermissionDenied
from functools import wraps

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'role'):
                if request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied  # 403 Forbidden
        return wrapper
    return decorator
