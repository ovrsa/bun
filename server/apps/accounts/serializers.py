import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from rest_framework import serializers

from .models import EmailVerificationToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("disabled account")

            user = authenticate(username=user.username, password=password)

            if not user:
                raise serializers.ValidationError("disabled account")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")

        data['user'] = user
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True) 


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data: dict):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("passwords do not match")
        
        try:
            validate_password(data['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.is_active = False
        user.save()

        # EmailVerificationToken を作成
        verification_token = EmailVerificationToken.objects.create(user=user, token=str(uuid.uuid4()))

        # メールを送信
        verification_url = self.context['request'].build_absolute_uri(
            reverse('email-verify', kwargs={'token': verification_token.token})
        )
        send_mail(
            subject='メールアドレスの確認',
            message=f'以下のリンクをクリックしてメールアドレスを確認してください: {verification_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user