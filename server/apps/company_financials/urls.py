from django.urls import path
from .views import FinancialSummaryView

urlpatterns = [
    path('', FinancialSummaryView.as_view(), name='company-financials'),
]
