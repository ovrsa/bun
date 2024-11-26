from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user_auth.Presentation.views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    LogoutView,
    EmailVerificationView,
    CheckAuthView,
    CSRFTokenView
)

urlpatterns = [
    path(
        'register/',
        UserRegistrationView.as_view(),
        name='register'
    ),
    path(
        'login/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'verify-email/<str:token>/',
        EmailVerificationView.as_view(),
        name='email-verify'
    ),
    path(
        'check-auth/',
        CheckAuthView.as_view(),
        name='check-auth'
    ),
    path(
        'csrf-token/',
        CSRFTokenView.as_view(),
        name='csrf_token'
        ),
]
