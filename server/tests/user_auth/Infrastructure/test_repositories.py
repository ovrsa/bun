import pytest
from unittest.mock import MagicMock, patch
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from apps.user_auth.Infrastructure.repositories import (
    CustomCookieJWTAuthentication,
    send_verification_email
)
from apps.user_auth.Domain.models import EmailVerificationToken

from django.conf import settings


@pytest.mark.django_db
class TestCustomCookieJWTAuthentication:
    def test_authenticate_success(self):
        # モックユーザーとトークンの作成
        user = User.objects.create_user(
            username="testuser",
            password="password123"
            )
        access_token = AccessToken.for_user(
            user
            )

        # モックリクエストの設定
        request = MagicMock()
        request.COOKIES = {'access_token': str(access_token)}

        # 認証の実行
        auth = CustomCookieJWTAuthentication()
        # ユーザーとトークンを取得
        result = auth.authenticate(request)

        # アサーション
        assert result is not None
        assert result[0] == user  # ユーザーが返されること
        assert str(result[1]) == str(access_token)  # トークンが一致すること

    def test_authenticate_failure_invalid_token(self):
        # 無効なトークンを設定
        request = MagicMock()
        request.COOKIES = {'access_token': 'invalid_token'}

        # 認証の実行
        auth = CustomCookieJWTAuthentication()

        # アサーション
        with pytest.raises(Exception, match='Invalid token'):
            auth.authenticate(request)

    def test_authenticate_failure_no_cookie(self):
        # クッキーが存在しない場合
        request = MagicMock()
        request.COOKIES = {}

        # 認証の実行
        auth = CustomCookieJWTAuthentication()
        result = auth.authenticate(request)

        # アサーション
        assert result is None  # Noneが返される


@pytest.mark.django_db
class TestSendVerificationEmail:
    @patch('apps.accounts.Infrastructure.repositories.send_mail')
    def test_send_verification_email(self, mock_send_mail):
        # モックユーザーとリクエストの作成
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://testserver/email-verify/"

        # メール送信の実行
        send_verification_email(user, request)

        # EmailVerificationTokenが作成されたことを確認
        token = EmailVerificationToken.objects.filter(user=user).first()
        assert token is not None
        assert token.user == user

        # メール送信が呼び出されたことを確認
        mock_send_mail.assert_called_once_with(
            subject='メールアドレスの確認',
            message=f'以下のリンクをクリックしてメールアドレスを確認してください: http://testserver/email-verify/',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
