from django.db import models
from django.contrib.auth.models import User
import uuid


class EmailVerificationToken(models.Model):
    """Email verification token model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EmailVerificationToken(user={self.user.username}, token={self.token})"
