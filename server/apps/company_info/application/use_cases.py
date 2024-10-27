from ..application import interfaces
from ..domain import services
from ..domain import repositories


class GetCompanyProfileUseCase:
    """企業情報を取得するユースケース"""

    def __init__(self, repository: repositories.CompanyProfileRepository, fetcher: interfaces.CompanyProfileFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker_ref):
        """ティッカーから企業情報を取得"""
        company_profile = self.repository.get_by_ticker(ticker_ref)

        if not company_profile:
            company_profile_data = self.fetcher.fetch(ticker_ref.ticker)
            if not company_profile_data:
                return None
            
            processed_data = services.CompanyProfileProcessor.process_raw_data(company_profile_data)
            company_profile = self.repository.save(processed_data, ticker_ref)

        return company_profile


class GetStockPriceUseCase:
    """株価データを取得するユースケース"""

    def __init__(self, repository: repositories.StockPriceRepository, fetcher: interfaces.StockPriceFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker):
        """ティッカーから株価データを取得"""
        stock_prices = self.repository.get_by_ticker(ticker)

        if stock_prices and stock_prices.exists():
            return stock_prices

        raw_data = self.fetcher.fetch(ticker).copy()
        if raw_data.empty:
            return None

        processed_data = services.StockPriceProcessor.process_raw_data(raw_data)
        self.repository.save(ticker, processed_data)

        return self.repository.get_by_ticker(ticker)


class GetCompanyFinancialsUseCase:
    """企業の財務データを取得するユースケース"""

    def __init__(self, repository: repositories.CompanyFinancialsRepository, fetcher: interfaces.CompanyFinancialsFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker):
        """ティッカーから企業の財務データを取得"""
        company_financials = self.repository.get_by_ticker(ticker)

        if company_financials and company_financials.exists():
            return company_financials
        
        financial_data = self.fetcher.fetch(ticker)
        if not financial_data:
            return None
        
        print(f"Financial data fetched successfully: {financial_data}")
        processed_data = services.FinancialDataProcessor.process_financial_data(
            financial_data['info'],
            financial_data['balance_sheet'],
            financial_data['cashflow']
        )
        print(f"Processed financial data successfully: {processed_data}")
        self.repository.save(ticker, processed_data)

        return self.repository.get_by_ticker(ticker)