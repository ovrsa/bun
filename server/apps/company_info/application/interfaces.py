from abc import ABC, abstractmethod
from ..models import CompanyProfile

class CompanyProfileFetcher(ABC):
    """ 企業情報を取得するためのインターフェース """
    @abstractmethod
    def fetch(self, ticker: str) -> CompanyProfile:
        """
        company_info.models.CompanyProfile

        Args:
            ticker (str): 銘柄コード

        Returns:
            company_info.models.CompanyProfile: 企業情報
        """
        
        pass

class StockPriceFetcher(ABC):
    """ 株価データを取得するためのインターフェース """
    @abstractmethod
    def fetch(self, ticker: str):
        """
        company_info.models.StockPrice

        Args:
            ticker (str): 銘柄コード

        Returns:
            List[Dict]: 株価データ
        """
        
        pass


class CompanyFinancialsFetcher(ABC):
    """ 企業の財務データを取得するためのインターフェース """
    @abstractmethod
    def fetch(self, ticker: str):
        """
        company_info.models.CompanyFinancials

        Args:
            ticker (str): 銘柄コード

        Returns:
            List[Dict]: 財務データ
        """
        
        pass