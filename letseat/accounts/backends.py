from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailBackend(ModelBackend):
    """Authenticate using email address + password."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username parameter comes from authenticate(...) call
        email = username or kwargs.get('email')
        if not email or not password:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
