from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.user_auth.Presentation.urls')),
    path('api/', include('apps.company_analytics.Presentation.urls')),
    path('api/', include('apps.stock_data.urls')),
]
