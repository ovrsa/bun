from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from . import models
from .infrastructure import repositories
from .infrastructure import external_services
from .application import use_cases
from .presentation import serializers


class CompanyProfileViewSet(viewsets.ModelViewSet):
    """Get company profile data"""

    queryset = models.CompanyProfile.objects.all()
    serializer_class = serializers.CompanyProfileSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs) -> Response:
        """
        
        Fetch company profile data for the requested ticker

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        
        """

        ticker = request.query_params.get('symbol', None)

        if not ticker:
            raise ValidationError("Ticker is not specified")

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.CompanyProfileRepositoryImpl()
        fetcher = external_services.YFinanceCompanyProfileFetcher()
        use_case = use_cases.GetCompanyProfileUseCase(repository, fetcher)

        company_profile = use_case.execute(ticker_ref)
        
        serializer = self.get_serializer(company_profile)
        
        return Response(serializer.data)


class StockPriceViewSet(viewsets.ModelViewSet):
    """Get stock price data"""

    queryset = models.StockPrice.objects.all()
    serializer_class = serializers.StockPriceSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs) -> Response:
        """
        
        Fetch stock price data for the requested ticker

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        
        """

        ticker = request.query_params.get('symbol', None)

        if not ticker:
            raise ValidationError("Ticker is not specified")
        
        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.StockPriceRepositoryImpl()
        fetcher = external_services.YFinanceStockPriceFetcher()
        use_case = use_cases.GetStockPriceUseCase(repository, fetcher)
        
        stock_prices = use_case.execute(ticker_ref.ticker)
        
        serializer = self.get_serializer(stock_prices, many=True)
        
        return Response(serializer.data)


class CompanyFinancialsViewSet(viewsets.ModelViewSet):
    """Get company financial data"""

    queryset = models.CompanyFinancials.objects.all()
    serializer_class = serializers.CompanyFinancialsSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs) -> Response:
        """

        Fetch company financial data for the requested ticker

        Args:   
            request (Request): Request object

        Returns:
            Response: Response object

        """

        ticker = request.query_params.get('symbol', None)

        if not ticker:
            raise ValidationError("Ticker is not specified")

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=ticker)
        repository = repositories.CompanyFinancialsRepositoryImpl()
        fetcher = external_services.YFinanceCompanyFinancialsFetcher()
        use_case = use_cases.GetCompanyFinancialsUseCase(repository, fetcher)

        company_financials = use_case.execute(ticker_ref.ticker)

        serializer = self.get_serializer(company_financials, many=True)

        return Response(serializer.data)
