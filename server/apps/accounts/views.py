import logging
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import EmailVerificationToken
from .serializers import LoginSerializer, UserRegistrationSerializer

logger = logging.getLogger(__name__)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomTokenObtainPairView(APIView):
    """Login view"""
    
    def post(self, request, *args, **kwargs):
        """
        Login

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"message": "ログインに成功しました。"}, status=status.HTTP_200_OK)
        return set_jwt_cookies(response, refresh, access)


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(APIView):
    """Refresh token view"""

    def post(self, request, *args, **kwargs):
        """
        Refresh token generate access token

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "does not exist refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            response = Response({"message": "generate access token"}, status=status.HTTP_200_OK)
            return set_jwt_cookies(response, refresh, access)

        except TokenError:
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LogoutView(APIView):
    """Logout view"""

    def post(self, request, *args, **kwargs):
        """
        case of logout

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.debug(f'token: {token}')
        except Exception as e:
            pass

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        return clear_jwt_cookies(response)


class EmailVerificationView(APIView):  
    """Email verification view"""
    def get(self, request, token, *args, **kwargs) -> Response:
        """
        Email verification process 

        Args:
            request (Request): Request object
            token (str): Token

        Returns:
            Response: Response object
        """
        
        try:
            verification_token = EmailVerificationToken.objects.get(token=str(token))
            user = verification_token.user
            user.is_active = True
            user.save()
            verification_token.delete()
            frontend_url = f"{os.environ('FRONTEND_URL')}/auth/verify-email/{token}"
            return HttpResponseRedirect(frontend_url)
        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "無効なトークンです。"}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(generics.CreateAPIView):
    """User registration view"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    """CSRF token view"""
    def get(self, request, *args, **kwargs) -> Response:
        """
        Get CSRF token

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        
        return Response({'detail': 'CSRF cookie set'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckAuthView(APIView):
    """Check authentication view"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Check authentication

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        
        return Response({'detail': '認証済み'}, status=status.HTTP_200_OK)
    

def set_jwt_cookies(response, refresh_token, access_token):
    """
    Set JWT cookies

    Args:
        response (Response): Response object
        refresh_token (RefreshToken): Refresh token object
        access_token (AccessToken): Access token object

    Returns:
        Response: Response object
    """
    
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )
    logger.debug(f'set_jwt_cookies: {response}')
    return response

def clear_jwt_cookies(response):
    """
    Clear JWT cookies

    Args:
        response (Response): Response object

    Returns:
        Response: Response object
    """
    
    response.set_cookie(
        key='access_token',
        value='',
        httponly=True,
        secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value='',
        httponly=True,
        secure=settings.SIMPLE_JWT['TOKEN_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['TOKEN_COOKIE_SAMESITE'],
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        path='/',
    )
    logger.debug(f'clear_jwt_cookies: {response}')
    return response

