from django.contrib.auth.backends import BaseBackend
from accounts.models import User

class UserBackend(BaseBackend):
    def authenticate(self, request, id=None, password=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None