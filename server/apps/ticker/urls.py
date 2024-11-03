from django.urls import path
from . import views

urlpatterns = [
    path('tickers/', views.nasdaq_ticker_list, name='nasdaq_ticker_list'),
]
