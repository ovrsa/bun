from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound, APIException

from . import models
from .infrastructure import repositories
from .infrastructure import external_services
from .application import use_cases
from .presentation import serializers


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = models.CompanyProfile.objects.all()
    serializer_class = serializers.CompanyProfileSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol', None)
        if not symbol:
            return super().list(request, *args, **kwargs)

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=symbol)
        repository = repositories.DjangoCompanyProfileRepository()
        fetcher = external_services.YFinanceCompanyProfileFetcher()
        use_case = use_cases.GetCompanyProfileUseCase(repository, fetcher)

        try:
            company_profile = use_case.execute(ticker_ref)
        except AuthenticationFailed:
            return Response(
                {"message": "認証に失敗しました"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        except TimeoutError:
            return Response(
                {"message": "サーバーが応答しませんでした。後でもう一度試してください"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        
        except Exception as e:
            return Response(
                {"message": f"データの取得中にエラーが発生しました: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        if not company_profile:
            return Response(
                {"message": "ティッカーから企業が見つかりませんでした"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(company_profile)
        return Response(serializer.data)


class StockPriceViewSet(viewsets.ModelViewSet):
    """ fetch stock price """
    queryset = models.StockPrice.objects.all()
    serializer_class = serializers.StockPriceSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol', None)
        if not symbol:
            return super().list(request, *args, **kwargs)
        
        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=symbol)
        respository = repositories.DjangoStockPriceRepository()
        fecher = external_services.YFinanceStockPriceFetcher()
        use_case = use_cases.GetStockPriceUseCase(respository, fecher)
        
        try:
            stock_price = use_case.execute(ticker_ref.ticker)
        except AuthenticationFailed:
            return Response(
                {"message": "認証に失敗しました"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        except TimeoutError:
            return Response(
                {"message": "サーバーが応答しませんでした。後でもう一度試してください"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        
        except Exception as e:
            return Response(
                {"message": f"データの取得中にエラーが発生しました: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        if not stock_price:
            return Response(
                {"message": "ティッカーから企業が見つかりませんでした"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(stock_price, many=True)
        return Response(serializer.data)


class CompanyFinancialsViewSet(viewsets.ModelViewSet):
    queryset = models.CompanyFinancials.objects.all()
    serializer_class = serializers.CompanyFinancialsSerializer
    lookup_field = 'ticker'

    def list(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol', None)
        if not symbol:
            return Response(
                {"message": "ティッカーシンボルが指定されていません"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticker_ref, created = models.TickerReference.objects.get_or_create(ticker=symbol)
        repository = repositories.DjangoCompanyFinancialsRepository()
        fetcher = external_services.YFinanceCompanyFinancialsFetcher()
        use_case = use_cases.GetCompanyFinancialsUseCase(repository, fetcher)

        try:
            company_financials = use_case.execute(ticker_ref.ticker)
        except AuthenticationFailed:
            return Response(
                {"message": "認証に失敗しました"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TimeoutError:
            return Response(
                {"message": "サーバーが応答しませんでした。後でもう一度試してください"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except Exception as e:
            return Response(
                {"message": f"データの取得中にエラーが発生しました: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not company_financials:
            return Response(
                {"message": "ティッカーから企業が見つかりませんでした"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(company_financials, many=True)
        return Response(serializer.data)
