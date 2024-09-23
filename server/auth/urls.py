from django.urls import path
from .views import CustomTokenObtainPairView
from .views import CustomTokenRefreshView
from .views import LogoutView
from .views import CSRFTokenView
from .views import CheckAuthView


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf_token'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
]
