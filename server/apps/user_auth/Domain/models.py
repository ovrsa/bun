import uuid

from django.contrib.auth.models import User
from django.db import models


class EmailVerificationToken(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification_tokens'
        )
    token = models.CharField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=36
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"EmailVerificationToken(user={self.user.username}, "
            f"token={self.token})"
        )
