from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from company_financials.core.use_case.get_company_financials_use_case import GetCompanyFinancialsUseCase

from company_financials.infra.repository.company_financials_repository import CompanyFinancialsRepository
from company_financials.infra.external.finnhub_client_factory import FinnhubClientFactory
from company_financials.infra.external.finnhub_financials_api import FinnhubFinancialsAPI

class FinancialSummaryRequestValidator:

    @staticmethod
    def validate(request):
        """
        リクエストパラメータのバリデーションを行う

        Args:
            request (Request): リクエスト

        Returns:
            Tuple[str, int, int]: シンボル、開始年、終了年のタプル
        """
        
        symbol = request.query_params.get('symbol')
        if not symbol:
            raise ValueError("Symbol parameter is required")
        
        start_year = request.query_params.get('start_year')
        end_year = request.query_params.get('end_year')

        try:
            if start_year:
                start_year = int(start_year)
            if end_year:
                end_year = int(end_year)

        except ValueError:
            raise ValueError("start_year and end_year must be integers")
        
        return symbol, start_year, end_year

class FinancialSummaryView(APIView):
    
    
    def get(self, request, *args, **kwargs):
        try:
            symbol, start_year, end_year = FinancialSummaryRequestValidator.validate(request)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        repository = CompanyFinancialsRepository()
        client_factory = FinnhubClientFactory()
        api_service = FinnhubFinancialsAPI(client=None)
        use_case = GetCompanyFinancialsUseCase(
            repository=repository,
            api_service=api_service,
            client_factory=client_factory
        )

        try:
            data = use_case.execute(symbol, start_year=start_year, end_year=end_year)
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
