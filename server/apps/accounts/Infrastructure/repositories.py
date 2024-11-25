from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


class CustomCookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request) -> tuple:
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken:
            raise exceptions.AuthenticationFailed('Invalid token')

        user = self.get_user(validated_token)
        if not user:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, validated_token)


def send_verification_email(user, request) -> None:
    """
    ユーザー登録時にメールアドレス確認用のメールを送信する

    Args:
        user (User): ユーザーオブジェクト
        request (Request): リクエストオブジェクト

    Returns:
        None
    """
    from apps.accounts.Domain.models import EmailVerificationToken
    import uuid

    token = EmailVerificationToken.objects.create(
        user=user,
        token=str(uuid.uuid4())
    )

    verification_url = request.build_absolute_uri(
        reverse('email-verify', kwargs={'token': token.token})
    )
    send_mail(
        subject='メールアドレスの確認',
        message=(
            '以下のリンクをクリックしてメールアドレスを確認してください: '
            f'{verification_url}'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
