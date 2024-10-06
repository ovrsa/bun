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
