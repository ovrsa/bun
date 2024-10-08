from .interfaces import CompanyProfileFetcher
from ..domain.repositories import CompanyProfileRepository

class GetCompanyProfileUseCase:
    """ 企業情報を取得するユースケース """
    def __init__(self, repository: CompanyProfileRepository, fetcher: CompanyProfileFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker: str):
        """ 銘柄コードから企業情報を取得する """
        company_profile = self.repository.get_by_ticker(ticker)

        if not company_profile:
            print(f"Fetching new data for {ticker} as it is not in cache or cache expired")
            company_profile = self.fetcher.fetch(ticker)
            self.repository.save(company_profile)

        return company_profile

class GetStockPriceUseCase:
    def __init__(self, repository, fetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker_symbol):
        """ 銘柄コードから株価データを取得する """
        stock_prices = self.repository.get_by_ticker(ticker_symbol)

        if stock_prices and stock_prices.exists():
            return stock_prices
        else:
            stock_data = self.fetcher.fetch(ticker_symbol)
            if not stock_data:
                return None
            self.repository.save(ticker_symbol, stock_data)
            return self.repository.get_by_ticker(ticker_symbol)
