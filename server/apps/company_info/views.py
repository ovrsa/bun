from rest_framework import mixins, viewsets
from rest_framework.response import Response
from .presentation.serializers import TickerQuerySerializer

from . import models
from .infrastructure import repositories
from .infrastructure import external_services
from .application import use_cases
from .presentation import serializers


class CompanyProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Get company profile data"""

    serializer_class = serializers.CompanyProfileSerializer

    def list(self, request, *args, **kwargs):

        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.CompanyProfileRepositoryImpl()
        fetcher = external_services.YFinanceCompanyProfileFetcher()
        use_case = use_cases.GetCompanyProfileUseCase(repository, fetcher)
        company_profile = use_case.execute(ticker_ref)

        serializer = self.get_serializer(company_profile)
        return Response(serializer.data)


class StockPriceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Get stock price data"""

    serializer_class = serializers.StockPriceSerializer

    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.StockPriceRepositoryImpl()
        fetcher = external_services.YFinanceStockPriceFetcher()
        use_case = use_cases.GetStockPriceUseCase(repository, fetcher)

        stock_prices = use_case.execute(ticker_ref.ticker)

        serializer = self.get_serializer(stock_prices, many=True)
        return Response(serializer.data)


class CompanyFinancialsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Get company financial data"""

    serializer_class = serializers.CompanyFinancialsSerializer

    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.CompanyFinancialsRepositoryImpl()
        fetcher = external_services.YFinanceCompanyFinancialsFetcher()
        use_case = use_cases.GetCompanyFinancialsUseCase(repository, fetcher)

        company_financials = use_case.execute(ticker_ref.ticker)

        serializer = self.get_serializer(company_financials, many=True)
        return Response(serializer.data)
