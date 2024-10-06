from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import CompanyProfile
from .models import StockPrice
from .models import CompanyFinancials
from .presentation.serializers import CompanyProfileSerializer
from .presentation.serializers import StockPriceSerializer
from .presentation.serializers import CompanyFinancialsSerializer
from .infrastructure.external_services import YFinanceCompanyProfileFetcher
from .application.use_cases import GetCompanyProfileUseCase
from .infrastructure.repositories import DjangoCompanyProfileRepository



class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs):
        respository = DjangoCompanyProfileRepository()
        fecher = YFinanceCompanyProfileFetcher()
        use_case = GetCompanyProfileUseCase(respository, fecher)

        symbol = request.query_params.get('symbol', None)
        if not symbol:
            return super().list(request, *args, **kwargs)

        company_profile = use_case.execute(symbol)
        if not company_profile:
            return Response({"detail": "Company profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(company_profile)
        return Response(serializer.data)



class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer


class CompanyFinancialsViewSet(viewsets.ModelViewSet):
    queryset = CompanyFinancials.objects.all()
    serializer_class = CompanyFinancialsSerializer

