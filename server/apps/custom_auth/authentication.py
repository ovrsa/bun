from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import exceptions
from django.conf import settings

class CustomCookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request) -> tuple:
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'])

        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed('No valid token found in cookie.')

        user = self.get_user(validated_token)
        if not user:
            raise exceptions.AuthenticationFailed('No user found for token.')

        return (user, validated_token)
