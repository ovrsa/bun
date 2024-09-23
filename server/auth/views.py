from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomTokenObtainPairView(APIView):
    """ ログイン用のビュー """

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # JWTトークンの生成
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # トークンをHTTPオンリークッキーにセット
        response = Response({"message": "ログインに成功しました。"}, status=status.HTTP_200_OK)

        # アクセストークンのクッキー設定
        response.set_cookie(
            key=settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'],
            value=str(access),
            httponly=settings.SIMPLE_JWT['TOKEN_COOKIE_HTTPONLY'],
            secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/',
        )

        # リフレッシュトークンのクッキー設定
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            path='/api/auth/',
        )

        return response


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        print('リフレッシュトークン:', refresh_token)

        if not refresh_token:
            print('リフレッシュトークンが見つかりません。')
            return Response({"detail": "リフレッシュトークンが見つかりません。"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token

            response = Response({"message": "トークンが更新されました。"}, status=status.HTTP_200_OK)

            # 新しいアクセストークンをクッキーにセット
            response.set_cookie(
                key=settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'],
                value=str(new_access),
                httponly=settings.SIMPLE_JWT['TOKEN_COOKIE_HTTPONLY'],
                secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                path='/',
            )

            print('新しいアクセストークンを発行しました。')
            return response

        except TokenError as e:
            print('トークンの更新に失敗:', e)
            return Response({"detail": "トークンの更新に失敗しました。"}, status=status.HTTP_401_UNAUTHORIZED)



@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    """ CSRFトークン取得用のビュー """

    def get(self, request, *args, **kwargs):
        return Response({'detail': 'CSRF cookie set'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LogoutView(APIView):
    """ ログアウト用のビュー """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'])

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
                print('リフレッシュトークンをブラックリストに登録しました。')
            except Exception as e:
                print('リフレッシュトークンのブラックリスト登録に失敗:', e)

        if access_token:
            try:
                access = AccessToken(access_token)
                access.blacklist()
                print('アクセストークンをブラックリストに登録しました。')
            except Exception as e:
                print('アクセストークンのブラックリスト登録に失敗:', e)

        response = Response({"message": "ログアウトしました。"}, status=status.HTTP_200_OK)
        response.delete_cookie(
            key=settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'],
            path='/',
            domain=None,
            samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        )
        response.delete_cookie(
            key='refresh_token',
            path='/api/auth/',
            domain=None,
            samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        )
        return response


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print('ユーザー:', request.user)
        return Response({'detail': 'Authenticated'}, status=200)
