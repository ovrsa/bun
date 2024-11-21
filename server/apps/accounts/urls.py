from django.urls import path

from .views import (CheckAuthView, CSRFTokenView, CustomTokenObtainPairView,
                    CustomTokenRefreshView, EmailVerificationView, LogoutView,
                    UserRegistrationView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf_token'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verify'),
]
