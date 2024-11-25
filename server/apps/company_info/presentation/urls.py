from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyProfileViewSet
from .views import StockPriceViewSet
from .views import CompanyFinancialsViewSet

router = DefaultRouter()
router.register(
    'company-profiles',
    CompanyProfileViewSet,
    basename='companyprofile'
    )
router.register(
    'stock-prices',
    StockPriceViewSet,
    basename='stockprice'
    )
router.register(
    'company-financials',
    CompanyFinancialsViewSet,
    basename='companyfinancials'
    )


urlpatterns = [
    path('', include(router.urls)),
]
