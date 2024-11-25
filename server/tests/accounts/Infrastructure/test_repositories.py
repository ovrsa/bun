import pytest
from unittest.mock import MagicMock, patch
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.Domain.models import EmailVerificationToken
from apps.accounts.Infrastructure.repositories import (
    CustomCookieJWTAuthentication,
    send_verification_email
)


@pytest.mark.django_db
class TestCustomCookieJWTAuthentication:
    def test_authenticate_success(self) -> None:
        """tokenでの認証が成功する場合のテスト"""

        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        access_token = AccessToken.for_user(user)

        request = MagicMock()
        request.COOKIES = {'access_token': str(access_token)}

        auth = CustomCookieJWTAuthentication()
        result = auth.authenticate(request)

        assert result is not None
        assert result[0] == user
        assert str(result[1]) == str(access_token)

    def test_authenticate_failure_invalid_token(self) -> None:
        """アクセストークンが不正な場合のテスト"""

        request = MagicMock()
        request.COOKIES = {'access_token': 'invalid_token'}

        auth = CustomCookieJWTAuthentication()

        with pytest.raises(Exception, match='Invalid token'):
            auth.authenticate(request)

    def test_authenticate_failure_no_cookie(self):
        """アクセストークンがない場合のテスト"""

        request = MagicMock()
        request.COOKIES = {}

        auth = CustomCookieJWTAuthentication()
        result = auth.authenticate(request)

        assert result is None


@pytest.mark.django_db
class TestSendVerificationEmail:
    @patch('apps.accounts.Infrastructure.repositories.send_mail')
    def test_send_verification_email(self, mock_send_mail: MagicMock) -> None:
        """メール送信のテスト"""

        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        request = MagicMock()
        request.build_absolute_uri.return_value = (
            "http://testserver/email-verify/"
        )

        send_verification_email(user, request)

        token = EmailVerificationToken.objects.filter(user=user).first()
        assert token is not None
        assert token.user == user

        mock_send_mail.assert_called_once_with(
            subject='メールアドレスの確認',
            message=(
                '以下のリンクをクリックしてメールアドレスを確認してください: '
                'http://testserver/email-verify/'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
