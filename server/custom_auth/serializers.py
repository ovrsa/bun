from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    """Syrializer for login"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate

        Args:
            data (dict): Request data

        Returns:
            dict: Validated data
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


from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ユーザー登録用のシリアライザー"""
    
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True) 


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        バリデーション

        Args:
            data (dict): リクエストデータ

        Returns:
            dict: バリデーション後のデータ
        """
        
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("パスワードが一致しません。")
        
        try:
            validate_password(data['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        return data

    def create(self, validated_data):
        """
        ユーザーを作成

        Args:
            validated_data (dict): バリデーション後のデータ

        Returns:
            User: 作成されたユーザー
        """
        
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.is_active = False
        user.save()

        return user
