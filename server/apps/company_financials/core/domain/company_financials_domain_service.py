from company_financials.core.repository.company_financials_repository import CompanyFinancialsRepository

class CompanyFinancialsDomainService:
    """会社の財務データの処理を行う"""

    def __init__(
        self,
        repository: CompanyFinancialsRepository,
        api_service,
        validator,
        extractor
    ):
        self.repository = repository
        self.api_service = api_service
        self.validator = validator
        self.extractor = extractor

    def process(self, symbol: str, start_year: int = None, end_year: int = None):
        """
        会社の財務データを取得する

        Args:
            symbol (str): シンボル
            start_year (int): 開始年
            end_year (int): 終了年

        Returns:
            CompanyFinancials: 会社の財務データ
        """
        self.validator.validate(symbol)

        cached_data = self.repository.fetch(symbol, start_year, end_year)
        if cached_data.exists():
            return cached_data

        raw_data = self.api_service.fetch_company_financials(symbol)
        extracted_data = self.extractor.extract_financial_info(raw_data)
        self.repository.save(extracted_data)
        return self.repository.fetch(symbol, start_year, end_year)

