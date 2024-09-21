from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework import generics, status
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailVerificationToken
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    """ ログイン用のビュー """

    def post(self, request, *args, **kwargs):
        """ログイン処理"""
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',  # 'Strict' / 'None'も選択可能
                max_age=5 * 60,  # 5分
                path='/',
            )

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',
                max_age=24 * 60 * 60,  # 1日
                path='/api/token/refresh/',
            )

            response.data.pop('access', None)
            response.data.pop('refresh', None)

        return response

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # HTTPS使用時はTrueに設定
                samesite='Lax',
                max_age=5 * 60,  # 5分
                path='/',
            )

            response.data.pop('access', None)
            response.data.pop('refresh', None)

        return response

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # ユーザーを非アクティブに設定
        user.is_active = False
        user.save()

        # メール認証トークンの生成
        token = EmailVerificationToken.objects.create(user=user)

        # 確認メールの送信
        verification_link = self.request.build_absolute_uri(
            reverse('email-verify', kwargs={'token': str(token.token)})
        )
        send_mail(
            subject='メールアドレスの確認',
            message=f'以下のリンクをクリックしてメールアドレスを確認してください：\n{verification_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "ユーザー登録が完了しました。確認メールを送信しましたので、メール内のリンクをクリックして手続きを完了してください。"},
            status=status.HTTP_201_CREATED
        )


    def perform_create(self, serializer):
        return serializer.save()

    def set_tokens_cookies(self, response, refresh, access):
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=False,  # HTTPS使用時はTrueに設定
            samesite='Lax',
            max_age=5 * 60,  # 5分
            path='/',
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,  # HTTPS使用時はTrueに設定
            samesite='Lax',
            max_age=24 * 60 * 60,  # 1日
            path='/api/token/refresh/',
        )
        
class EmailVerificationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            user = verification_token.user
            user.is_active = True
            user.save()
            verification_token.delete()
            return Response({"message": "メールアドレスの確認が完了しました。"}, status=status.HTTP_200_OK)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "無効なトークンです。"}, status=status.HTTP_400_BAD_REQUEST)
