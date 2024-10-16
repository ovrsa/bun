from .interfaces import CompanyProfileFetcher
from ..domain.repositories import CompanyProfileRepository
from .interfaces import StockPriceFetcher
from ..domain.repositories import StockPriceRepository
from .interfaces import CompanyFinancialsFetcher
from ..domain.repositories import CompanyFinancialsRepository


class GetCompanyProfileUseCase:
    def __init__(self, repository, fetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker_ref):
        """ティッカーコードから企業情報を取得"""
        company_profile = self.repository.get_by_ticker(ticker_ref)

        if not company_profile:
            print(f"Fetching new data for {ticker_ref.ticker} as it is not in cache or cache expired")
            company_profile_data = self.fetcher.fetch(ticker_ref.ticker)
            if not company_profile_data:
                return None
            company_profile = self.repository.save(company_profile_data, ticker_ref)

        return company_profile


class GetStockPriceUseCase:
    """ 株価データを取得するユースケース """
    def __init__(self, repository: StockPriceRepository, fetcher: StockPriceFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker):
        """ 銘柄コードから株価データを取得する """
        stock_prices = self.repository.get_by_ticker(ticker)

        if stock_prices and stock_prices.exists():
            return stock_prices
        else:
            stock_data = self.fetcher.fetch(ticker)
            if not stock_data:
                return None
            self.repository.save(ticker, stock_data)
            return self.repository.get_by_ticker(ticker)


class GetCompanyFinancialsUseCase:
    """ 企業の財務データを取得するユースケース """
    def __init__(self, repository: CompanyFinancialsRepository, fetcher: CompanyFinancialsFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker):
        """ 銘柄コードから企業の財務データを取得する """
        company_financials = self.repository.get_by_ticker(ticker)

        if company_financials and company_financials.exists():
            return company_financials
        else:
            financial_data = self.fetcher.fetch(ticker)
            if not financial_data:
                return None
            self.repository.save(ticker, financial_data)
            return self.repository.get_by_ticker(ticker)