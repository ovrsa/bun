
from ..Infrastructure.external_services import (
    YFinanceCompanyProfileFetcher,
    YFinanceStockPriceFetcher,
    YFinanceCompanyFinancialsFetcher
)
from ..Domain.services import (
    CompanyProfileProcessor,
    StockPriceProcessor,
    FinancialDataProcessor
)
from ..Domain.models import (
    TickerReference,
    CompanyProfile,
    StockPrice,
    CompanyFinancials
    )


class GetCompanyProfileUseCase:

    def execute(self, ticker: str) -> CompanyProfile:
        # tickerを一意に識別するための参照を取得
        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        company_profile, created = CompanyProfile.objects.get_or_create(
            ticker=ticker_ref,
            defaults=self._update_company_profile(ticker_ref)
        )
        return company_profile

    def _update_company_profile(self, ticker_ref):
        # 24時間のキャッシュが切れた場合、新たにデータを取得
        fetcher = YFinanceCompanyProfileFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
        processed_data = CompanyProfileProcessor.process_raw_data(raw_data)

        company_profile, _ = CompanyProfile.objects.update_or_create(
            ticker=ticker_ref,
            defaults=processed_data
        )
        return company_profile


class GetStockPriceUseCase:

    def execute(self, ticker: str) -> list:

        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        stock_prices = StockPrice.objects.filter(ticker=ticker_ref)

        if not stock_prices.exists():
            stock_prices = self._update_stock_prices(ticker_ref)
        return stock_prices

    def _update_stock_prices(self, ticker_ref):

        fetcher = YFinanceStockPriceFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
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

    def execute(self, ticker: str) -> list:

        ticker_ref, _ = TickerReference.objects.get_or_create(ticker=ticker)
        financials = CompanyFinancials.objects.filter(ticker=ticker_ref)

        if not financials.exists():
            financials = self._update_company_financials(ticker_ref)
        return financials

    def _update_company_financials(self, ticker_ref):

        fetcher = YFinanceCompanyFinancialsFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)

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
