from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from ..Domain import models
from ..Domain import services
from ..Infrastructure import external_services
from ..Presentation.serializers import TickerQuerySerializer
from ..Presentation import serializers


class CompanyProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.CompanyProfileSerializer

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, _ = models.TickerReference.objects.get_or_create(ticker=ticker)
        company_profile, _ = models.CompanyProfile.objects.get_or_create(
            ticker=ticker_ref,
            defaults=self.update_company_profile(ticker_ref)
        )

        serializer = self.get_serializer(company_profile)
        return Response(serializer.data)

    def update_company_profile(self, ticker_ref):
        fetcher = external_services.YFinanceCompanyProfileFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
        processed_data = services.CompanyProfileProcessor.process_raw_data(raw_data)

        company_profile, _ = models.CompanyProfile.objects.update_or_create(
            ticker=ticker_ref,
            defaults=processed_data
        )
        return company_profile


class StockPriceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.StockPriceSerializer

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, _ = models.TickerReference.objects.get_or_create(ticker=ticker)
        stock_prices = models.StockPrice.objects.filter(ticker=ticker_ref)

        # データが存在しない場合は新規取得・保存
        if not stock_prices.exists():
            stock_prices = self.update_stock_prices(ticker_ref)

        serializer = self.get_serializer(stock_prices, many=True)
        return Response(serializer.data)

    def update_stock_prices(self, ticker_ref):
        fetcher = external_services.YFinanceStockPriceFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
        processed_data = services.StockPriceProcessor.process_raw_data(raw_data)

        stock_prices = [
            models.StockPrice.objects.update_or_create(
                ticker=ticker_ref,
                date=data['date'],
                defaults=data
            )[0]
            for data in processed_data
        ]
        return stock_prices


class CompanyFinancialsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.CompanyFinancialsSerializer

    @method_decorator(cache_page(60 * 60 * 24))  # 24時間キャッシュ
    def list(self, request, *args, **kwargs):
        query_serializer = TickerQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        ticker = query_serializer.validated_data['symbol']

        ticker_ref, _ = models.TickerReference.objects.get_or_create(ticker=ticker)
        financials = models.CompanyFinancials.objects.filter(ticker=ticker_ref)

        # データが存在しない場合は新規取得・保存
        if not financials.exists():
            financials = self.update_company_financials(ticker_ref)

        serializer = self.get_serializer(financials, many=True)
        return Response(serializer.data)

    def update_company_financials(self, ticker_ref):
        fetcher = external_services.YFinanceCompanyFinancialsFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)

        # 財務データとして必要なデータを取得
        balance_sheet = raw_data.get('balance_sheet')
        cashflow = raw_data.get('cashflow')
        income_stmt = raw_data.get('income_stmt')

        if any(df is None or df.empty for df in [balance_sheet, cashflow, income_stmt]):
            raise ValueError("Incomplete or empty financial data from external API")

        processed_data = services.FinancialDataProcessor.process_raw_data(
            balance_sheet, cashflow, income_stmt
        )

        company_financials = [
            models.CompanyFinancials.objects.update_or_create(
                ticker=ticker_ref,
                fiscal_year=data['fiscal_year'],
                defaults=data
            )[0]
            for data in processed_data.values()
        ]
        return company_financials
