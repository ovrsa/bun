import pytest
from unittest.mock import MagicMock
from django.contrib.auth import get_user_model
from apps.user_auth.Application.use_cases import register_user
from apps.user_auth.Domain.models import EmailVerificationToken

User = get_user_model()


# TODO: テストが通らないので修正
@pytest.mark.django_db
def test_register_user_creates_inactive_user():
    # 既存データの削除
    User.objects.filter(username="testuser").delete()
    print(f'[DEBUG] User.objects.all(): {User.objects.all()}')
    EmailVerificationToken.objects.all().delete()

    # モックデータの準備
    validated_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "password_confirm": "password123",
    }
    request_mock = MagicMock()
    print(f'[DEBUG] request_mock: {request_mock}')
    request_mock.build_absolute_uri.return_value = (
        "http://testserver/email-verify/"
    )

    # 実行
    result = register_user(validated_data, request_mock)
    print(f'[DEBUG] result: {result}')

    # アサーション
    assert result.username == "testuser"
    assert result.is_active is False

    # EmailVerificationTokenが作成されているか確認
    token = EmailVerificationToken.objects.filter(user=result).first()
    assert token is not None
    assert token.user == result
