from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    """ログイン用のシリアライザー"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        バリデーション

        Args:
            data (dict): リクエストデータ

        Returns:
            dict: バリデーション後のデータ
        """
        
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("無効なメールアドレスまたはパスワード。")

            user = authenticate(username=user.username, password=password)

            if not user:
                raise serializers.ValidationError("無効なメールアドレスまたはパスワード。")
        else:
            raise serializers.ValidationError("メールアドレスとパスワードを提供してください。")

        data['user'] = user
        return data
