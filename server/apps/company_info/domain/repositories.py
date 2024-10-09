from abc import ABC, abstractmethod
from ..models import CompanyProfile

class CompanyProfileRepository(ABC):
    """ 企業情報のリポジトリインターフェース """
    @abstractmethod
    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """ 銘柄コードから企業情報を取得する """
        pass

    @abstractmethod
    def save(self, company_profile: CompanyProfile) -> None:
        """ 企業情報を保存する """
        pass


class StockPriceRepository(ABC):
    """ 株価データのリポジトリインターフェース """
    @abstractmethod
    def get_by_ticker(self, ticker: str):
        """ 銘柄コードから株価データを取得する """
        pass

    @abstractmethod
    def save(self, ticker: str, stock_prices):
        """ 株価データを保存する """
        pass


class CompanyFinancialsRepository(ABC):
    """ 企業の財務データのリポジトリインターフェース """
    @abstractmethod
    def get_by_ticker(self, ticker: str):
        """ 銘柄コードから企業の財務データを取得する """
        pass

    @abstractmethod
    def save(self, ticker: str, financial_data):
        """ 財務データを保存する """
        pass