from abc import ABC, abstractmethod
from ..models import CompanyProfile

class CompanyProfileRepository(ABC):
    """Company profile repository interface"""
    @abstractmethod
    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """Get company profile data for ticker"""
        pass

    @abstractmethod
    def save(self, company_profile: CompanyProfile) -> None:
        """Save company profile data"""
        pass


class StockPriceRepository(ABC):
    """Stock price repository interface"""
    @abstractmethod
    def get_by_ticker(self, ticker: str):
        """Get stock price data for ticker"""
        pass

    @abstractmethod
    def save(self, ticker: str, stock_prices):
        """Save stock price data"""
        pass


class CompanyFinancialsRepository(ABC):
    """Company financials repository interface"""
    @abstractmethod
    def get_by_ticker(self, ticker: str):
        """Get financial data for ticker"""
        pass

    @abstractmethod
    def save(self, ticker: str, financial_data):
        """Save financial data"""
        pass