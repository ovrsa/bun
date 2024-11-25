from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from ..Application.use_cases import (
    GetCompanyProfileUseCase,
    GetStockPriceUseCase,
    GetCompanyFinancialsUseCase
)
from ..Presentation.serializers import TickerQuerySerializer
from ..Presentation import serializers


class CompanyProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.CompanyProfileSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_case = GetCompanyProfileUseCase()

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        company_profile = self.use_case.execute(ticker)
        serializer = self.get_serializer(company_profile)
        return Response(serializer.data)


class StockPriceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.StockPriceSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_case = GetStockPriceUseCase()

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        stock_prices = self.use_case.execute(ticker)
        serializer = self.get_serializer(stock_prices, many=True)
        return Response(serializer.data)


class CompanyFinancialsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.CompanyFinancialsSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_case = GetCompanyFinancialsUseCase()

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        financials = self.use_case.execute(ticker)
        serializer = self.get_serializer(financials, many=True)
        return Response(serializer.data)
