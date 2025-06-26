from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CommonUtils:
    @staticmethod
    def create_access(user: User):
        try:
            if not user.is_active:
                raise AuthenticationFailed("The user is not active!")
            refresh = RefreshToken.for_user(user)
            return {"refresh": str(refresh), "access": str(refresh.access_token)}
        except Exception as e:
            raise AuthenticationFailed(f"Unexpected error while generating tokens{e}")
