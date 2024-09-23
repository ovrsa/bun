from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import exceptions
from django.conf import settings

class CustomCookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'])
        print('アクセストークン:', access_token)

        if not access_token:
            print('アクセストークンが見つかりません。')
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken as e:
            print('アクセストークンの検証に失敗:', e)
            raise exceptions.AuthenticationFailed('アクセストークンが無効です。')

        user = self.get_user(validated_token)
        if not user:
            print('ユーザーが見つかりません。')
            raise exceptions.AuthenticationFailed('ユーザーが見つかりません。')

        print('認証成功:', user)
        return (user, validated_token)
