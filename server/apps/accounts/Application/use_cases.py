from django.contrib.auth.models import User
from django.urls import reverse
from apps.accounts.Domain.models import EmailVerificationToken
from apps.accounts.Infrastructure.repositories import send_verification_email
import uuid


def register_user(validated_data, request) -> User:
    validated_data.pop('password_confirm')
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data.get('email'),
        password=validated_data['password']
    )
    user.is_active = False
    user.save()

    token = EmailVerificationToken.objects.create(
        user=user,
        token=str(uuid.uuid4())
    )

    verification_url = request.build_absolute_uri(
        reverse('email-verify', kwargs={'token': token.token})
    )
    send_verification_email(user.email, verification_url)
    return user


def verify_email_token(token) -> bool:
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        user = verification_token.user
        user.is_active = True
        user.save()
        verification_token.delete()
        return True
    except EmailVerificationToken.DoesNotExist:
        return False
