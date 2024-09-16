from ..repository.company_financials_repository import CompanyFinancialsRepository
from ..domain.company_financials_domain_service import CompanyFinancialsDomainService
from ..domain.company_symbol_validator import CompanySymbolValidator
from ..domain.financial_data_extractor import FinancialDataExtractor

from company_financials.web.serializers.company_financials_serializer import CompanyFinancialsSerializer

class GetCompanyFinancialsUseCase:
    """会社の財務データを取得するユースケース"""

    def __init__(
        self,
        repository: CompanyFinancialsRepository,
        api_service,
        client_factory
    ):
        self.client_factory = client_factory
        self.repository = repository
        self.api_service = api_service

    def execute(self, symbol: str, start_year: int = None, end_year: int = None) -> dict:
        """
        会社の財務データを取得する

        Args:
            symbol (str): シンボル
            start_year (int): 開始年
            end_year (int): 終了年

        Returns:
            dict: 会社の財務データ
        """
        
        client = self.client_factory.create_client()
        self.api_service.client = client

        validator = CompanySymbolValidator()
        extractor = FinancialDataExtractor()
        domain_service = CompanyFinancialsDomainService(
            repository=self.repository,
            api_service=self.api_service,
            validator=validator,
            extractor=extractor
        )

        financials = domain_service.process(symbol, start_year, end_year)
        serializer = CompanyFinancialsSerializer(financials, many=True)
        return {
            "ticker": symbol,
            "start_year": start_year,
            "end_year": end_year,
            "total": len(serializer.data),
            "financials": serializer.data,
        }