from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(serializers.Serializer):
    """Syrializer for login"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict):
        """Validate"""
        
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
    """Syrializer for user registration"""
    
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True) 


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data: dict):
        """Validate"""

        
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("passwords do not match")
        
        try:
            validate_password(data['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        
        return data

    def create(self, validated_data: dict):
        """
        Create user

        Args:
            validated_data (dict)

        Returns:
            User: User object
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
