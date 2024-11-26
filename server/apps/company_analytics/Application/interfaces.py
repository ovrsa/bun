from abc import ABC, abstractmethod
from ..Domain.models import CompanyProfile


class CompanyProfileFetcher(ABC):

    @abstractmethod
    def fetch(self, ticker: str) -> CompanyProfile:
        pass


class StockPriceFetcher(ABC):

    @abstractmethod
    def fetch(self, ticker: str):
        pass


class CompanyFinancialsFetcher(ABC):

    @abstractmethod
    def fetch(self, ticker: str):
        pass
