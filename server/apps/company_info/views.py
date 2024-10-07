from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import CompanyProfile
from .infrastructure.repositories import DjangoCompanyProfileRepository
from .application.use_cases import GetCompanyProfileUseCase
from .infrastructure.external_services import YFinanceCompanyProfileFetcher
from .presentation.serializers import CompanyProfileSerializer

from .models import StockPrice
from .infrastructure.repositories import DjangoStockPriceRepository
from .application.use_cases import GetStockPriceUseCase
from .presentation.serializers import StockPriceSerializer
from .infrastructure.external_services import YFinanceStockPriceFetcher

from .models import CompanyFinancials
from .presentation.serializers import CompanyFinancialsSerializer


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
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs):
        respository = DjangoStockPriceRepository()
        fecher = YFinanceStockPriceFetcher()
        use_case = GetStockPriceUseCase(respository, fecher)

        symbol = request.query_params.get('symbol', None)
        if not symbol:
            return super().list(request, *args, **kwargs)
        
        stock_price = use_case.execute(symbol)
        if not stock_price:
            return Response({"detail": "Stock price not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(stock_price, many=True)
        return Response(serializer.data)


class CompanyFinancialsViewSet(viewsets.ModelViewSet):
    queryset = CompanyFinancials.objects.all()
    serializer_class = CompanyFinancialsSerializer

