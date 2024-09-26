from django.urls import path
from .views import UserRegistrationView
from .views import LogoutView
from .views import CustomTokenObtainPairView
from .views import CustomTokenRefreshView
from .views import CSRFTokenView
from .views import CheckAuthView
from .views import EmailVerificationView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf_token'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uuid:token>/', EmailVerificationView.as_view(), name='email-verify'),
]
