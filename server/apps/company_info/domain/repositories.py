from abc import ABC, abstractmethod
from ..models import CompanyProfile


class CompanyProfileRepository(ABC):

    @abstractmethod
    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        pass

    @abstractmethod
    def save(self, company_profile: CompanyProfile) -> None:
        pass


class StockPriceRepository(ABC):

    @abstractmethod
    def get_by_ticker(self, ticker: str):
        pass

    @abstractmethod
    def save(self, ticker: str, stock_prices):
        pass


class CompanyFinancialsRepository(ABC):

    @abstractmethod
    def get_by_ticker(self, ticker: str):
        pass

    @abstractmethod
    def save(self, ticker: str, financial_data):
        pass
