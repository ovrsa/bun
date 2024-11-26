from django.urls import path
from . import views

urlpatterns = [
    path('tickers/', views.NasdaqTickerListView.as_view(), name='nasdaq_ticker_list'),
]
