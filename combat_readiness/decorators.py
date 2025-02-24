from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied  # 403 Forbidden
        return wrapper
    return decorator
