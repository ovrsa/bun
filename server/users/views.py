# from rest_framework import generics
# from django.contrib.auth.models import User

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from .serializers import UserRegistrationSerializer

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import send_mail
# from django.urls import reverse
# from .models import EmailVerificationToken  # メール認証を実装する場合

# @method_decorator(csrf_exempt, name='dispatch')
# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)

#         # トークンの生成
#         refresh = RefreshToken.for_user(user)
#         token_data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }

#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {"message": "ユーザー登録が成功しました。", "token": token_data},
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

#     def perform_create(self, serializer):
#         return serializer.save()

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings

# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:
#             # アクセストークンをHTTPオンリークッキーにセット
#             access_token = response.data.get('access')
#             refresh_token = response.data.get('refresh')

#             # アクセストークンのクッキー設定
#             response.set_cookie(
#                 key=settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'],
#                 value=access_token,
#                 httponly=settings.SIMPLE_JWT['TOKEN_COOKIE_HTTPONLY'],
#                 secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
#                 samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
#                 max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
#                 path='/',
#             )

#             # リフレッシュトークンも必要に応じてセット
#             response.set_cookie(
#                 key='refresh_token',
#                 value=refresh_token,
#                 httponly=True,
#                 secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
#                 samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
#                 max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
#                 path='/api/token/refresh/',
#             )

#             # レスポンスからトークン情報を削除（セキュリティ向上）
#             response.data.pop('access', None)
#             response.data.pop('refresh', None)
#         return response


# users/views.py

from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# トークン取得ビューのカスタマイズ
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # アクセストークンをHTTPオンリークッキーにセット
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',  # 'Strict' / 'None'も選択可能
                max_age=5 * 60,  # 5分
                path='/',
            )

            # リフレッシュトークンもクッキーにセット
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',
                max_age=24 * 60 * 60,  # 1日
                path='/api/token/refresh/',
            )

            # レスポンスからトークン情報を削除
            response.data.pop('access', None)
            response.data.pop('refresh', None)

        return response

# トークンリフレッシュビューのカスタマイズ
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')

            # 新しいアクセストークンをクッキーにセット
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',
                max_age=5 * 60,  # 5分
                path='/',
            )

            # レスポンスからトークン情報を削除
            response.data.pop('access', None)
            response.data.pop('refresh', None)

        return response

# ユーザー登録ビューのカスタマイズ
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # トークンの生成
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # トークンをクッキーにセット
        response = Response(
            {"message": "ユーザー登録が成功しました。"},
            status=status.HTTP_201_CREATED,
        )
        self.set_tokens_cookies(response, refresh, access)

        return response

    def perform_create(self, serializer):
        return serializer.save()

    def set_tokens_cookies(self, response, refresh, access):
        # アクセストークンのクッキー設定
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=False,  # HTTPS使用時はTrueに設定
            samesite='Lax',
            max_age=5 * 60,  # 5分
            path='/',
        )

        # リフレッシュトークンのクッキー設定
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,  # HTTPS使用時はTrueに設定
            samesite='Lax',
            max_age=24 * 60 * 60,  # 1日
            path='/api/token/refresh/',
        )
