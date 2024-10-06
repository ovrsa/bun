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
