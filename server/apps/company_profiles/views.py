from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, AuthenticationFailed, APIException
from company_profiles.services.finnhub_service import FinnhubService


class CompanyProfileView(APIView):
    """API endpoint to get and save company profile data from Finnhub."""

    def get(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol')
        print(f'params: %s' % symbol)
        if not symbol:
            return Response({"error": "Symbol parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = FinnhubService()
        try:
            profile = service.get_company_profile(symbol)

            if profile:
                profile_data = {
                    'company_name': profile.company_name,
                    'ticker': profile.ticker,
                    'country': profile.country,
                    'currency': profile.currency,
                    'exchange': profile.exchange,
                    'ipo_date': profile.ipo_date,
                    'market_capitalization': profile.market_capitalization,
                    'phone': profile.phone,
                    'share_outstanding': profile.share_outstanding,
                    'website_url': profile.website_url,
                    'logo_url': profile.logo_url,
                    'finnhub_industry': profile.finnhub_industry,
                }
                return Response(profile_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Profile data could not be retrieved."}, status=status.HTTP_404_NOT_FOUND)

        except NotFound as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except TimeoutError as e:
            return Response({"message": str(e)}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"message": f"データの取得中にエラーが発生しました: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
