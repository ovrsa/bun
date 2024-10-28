from ..application import interfaces
from ..domain import services
from ..domain import repositories


class GetCompanyProfileUseCase:
    """Company Profile Use Case"""

    def __init__(self, repository: repositories.CompanyProfileRepository, fetcher: interfaces.CompanyProfileFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker_ref: str) -> repositories.CompanyProfileRepository:
        """Fetch company profile data for the requested ticker"""
        company_profile = self.repository.get_by_ticker(ticker_ref)

        if not company_profile:
            company_profile_data = self.fetcher.fetch(ticker_ref.ticker)
            if not company_profile_data:
                return None
            
            processed_data = services.CompanyProfileProcessor.process_raw_data(company_profile_data)
            company_profile = self.repository.save(processed_data, ticker_ref)

        return company_profile


class GetStockPriceUseCase:
    """Stock Price Use Case"""

    def __init__(self, repository: repositories.StockPriceRepository, fetcher: interfaces.StockPriceFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker: str) -> repositories.StockPriceRepository:
        """Fetch stock price data for the requested ticker"""
        stock_prices = self.repository.get_by_ticker(ticker)

        if stock_prices and len(stock_prices) > 0:
            return stock_prices

        raw_data = self.fetcher.fetch(ticker).copy()
        if raw_data.empty:
            return None

        processed_data = services.StockPriceProcessor.process_raw_data(raw_data)
        self.repository.save(ticker, processed_data)

        return self.repository.get_by_ticker(ticker)


class GetCompanyFinancialsUseCase:
    """Company Financials Use Case"""

    def __init__(self, repository: repositories.CompanyFinancialsRepository, fetcher: interfaces.CompanyFinancialsFetcher):
        self.repository = repository
        self.fetcher = fetcher

    def execute(self, ticker: str) -> repositories.CompanyFinancialsRepository:
        """Fetch financial data for the requested ticker"""
        company_financials = self.repository.get_by_ticker(ticker)

        if company_financials and len(company_financials) > 0:
            return company_financials
        
        financial_data = self.fetcher.fetch(ticker)
        if not financial_data:
            return None
        
        processed_data = services.FinancialDataProcessor.process_financial_data(
            financial_data['info'],
            financial_data['balance_sheet'],
            financial_data['cashflow']
        )
        self.repository.save(ticker, processed_data)

        return self.repository.get_by_ticker(ticker)