from .client_initializer import ClientInitializer
from .company_profile_validator import CompanyProfileValidator
from .company_profile_repository import CompanyProfileRepository
from .finnhub_api_service import FinnhubAPIService


class FinnhubService:
    """Finnhub APIと連携して会社概要を取得するサービス"""
    def __init__(self):
        self.client = ClientInitializer().client
        self.validator = CompanyProfileValidator()
        self.repository = CompanyProfileRepository()
        self.api_service = FinnhubAPIService(self.client)

    def get_company_profile(self, symbol: str):
        """指定されたシンボルに対応する会社概要を取得する"""
        
        self.validator.validate_symbol(symbol)

        cached_profile = self.repository.get_cached_profile(symbol)
        if cached_profile:
            return cached_profile

        profile_data = self.api_service.fetch_company_profile(symbol)
        self.validator.validate_profile_data(profile_data)
        return self.repository.save_company_profile(profile_data)
