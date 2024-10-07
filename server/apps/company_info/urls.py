from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyProfileViewSet
from .views import StockPriceViewSet
from .views import CompanyFinancialsViewSet

router = DefaultRouter()
router.register(r'company-profiles', CompanyProfileViewSet, basename='companyprofile')
router.register(r'stock-prices', StockPriceViewSet, basename='stockprice')
router.register(r'company-financials', CompanyFinancialsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
