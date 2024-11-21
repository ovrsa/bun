from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomCookieJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication class"""
    
    def authenticate(self, request):
        """
        Authenticate user

        Args:
            request (Request): Request object

        Returns:
            Tuple: User and token
        """
        
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken:
            raise exceptions.AuthenticationFailed('Invalid token')

        user = self.get_user(validated_token)
        if not user:
            raise exceptions.AuthenticationFailed('No user found for token')

        return (user, validated_token)