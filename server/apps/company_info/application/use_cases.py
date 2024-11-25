from ..Domain.models import (
    TickerReference,
    CompanyProfile,
    StockPrice,
    CompanyFinancials
)
from ..Domain.services import (
    CompanyProfileProcessor,
    StockPriceProcessor,
    FinancialDataProcessor
)
from ..Application.interfaces import (
    CompanyProfileFetcher,
    StockPriceFetcher,
    CompanyFinancialsFetcher
)


class GetCompanyProfileUseCase:
    def __init__(self, fetcher: CompanyProfileFetcher):
        self.fetcher = fetcher

    def execute(self, ticker: str) -> CompanyProfile:
        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        company_profile, created = CompanyProfile.objects.get_or_create(
            ticker=ticker_ref,
            defaults=self._update_company_profile(ticker_ref)
        )
        return company_profile

    def _update_company_profile(self, ticker_ref):
        raw_data = self.fetcher.fetch(ticker_ref.ticker)
        processed_data = CompanyProfileProcessor.process_raw_data(raw_data)

        company_profile, _ = CompanyProfile.objects.update_or_create(
            ticker=ticker_ref,
            defaults=processed_data
        )
        return company_profile


class GetStockPriceUseCase:
    def __init__(self, fetcher: StockPriceFetcher):
        self.fetcher = fetcher

    def execute(self, ticker: str) -> list:

        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        stock_prices = StockPrice.objects.filter(ticker=ticker_ref)

        if not stock_prices.exists():
            stock_prices = self._update_stock_prices(ticker_ref)
        return stock_prices

    def _update_stock_prices(self, ticker_ref):
        raw_data = self.fetcher.fetch(ticker_ref.ticker)
        processed_data = StockPriceProcessor.process_raw_data(raw_data)

        stock_prices = [
            StockPrice.objects.update_or_create(
                ticker=ticker_ref,
                date=data['date'],
                defaults=data
            )[0]
            for data in processed_data
        ]
        return stock_prices


class GetCompanyFinancialsUseCase:
    def __init__(self, fetcher: CompanyFinancialsFetcher):
        self.fetcher = fetcher

    def execute(self, ticker: str) -> list:

        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        financials = CompanyFinancials.objects.filter(ticker=ticker_ref)

        if not financials.exists():
            financials = self._update_company_financials(ticker_ref)
        return financials

    def _update_company_financials(self, ticker_ref):
        raw_data = self.fetcher.fetch(ticker_ref.ticker)
        balance_sheet = raw_data.get('balance_sheet')
        cashflow = raw_data.get('cashflow')
        income_stmt = raw_data.get('income_stmt')

        if any(df is None or df.empty for df in [
                balance_sheet,
                cashflow,
                income_stmt
                ]):
            raise ValueError("Incomplete or empty financial data")

        processed_data = FinancialDataProcessor.process_raw_data(
                balance_sheet,
                cashflow,
                income_stmt
                )

        financials = [
            CompanyFinancials.objects.update_or_create(
                ticker=ticker_ref,
                fiscal_year=data['fiscal_year'],
                defaults=data
            )[0]
            for data in processed_data.values()
        ]
        return financials
