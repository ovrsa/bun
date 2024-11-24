from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.Presentation.serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.accounts.Application.use_cases import (
    register_user,
    verify_email_token
)
from apps.accounts.Infrastructure.utils import (
    set_jwt_cookies,
    clear_jwt_cookies
)


class UserRegistrationView(APIView):

    def post(self, request) -> Response:
        serializer = UserRegistrationSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            register_user(serializer.validated_data, request)
            return Response(
                {"message": "ユーザー登録が成功しました。"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(
            self, request,
            response, *args, **kwargs
            ) -> Response:
        if response.status_code == 200 and 'access' in response.data:
            set_jwt_cookies(
                response,
                response.data['access'],
                response.data['refresh']
                )
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):

    def post(self, request):
        response = Response(
            {"message": "ログアウトしました。"},
            status=status.HTTP_200_OK
        )
        clear_jwt_cookies(response)
        return response


class EmailVerificationView(APIView):

    def get(self, request, token):
        if verify_email_token(token):
            return Response(
                {"message": "メール確認が完了しました。"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "無効なトークンです。"},
            status=status.HTTP_400_BAD_REQUEST
        )


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'detail': '認証済み'}, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'CSRF cookie set'})
