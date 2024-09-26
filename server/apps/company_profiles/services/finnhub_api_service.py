import logging

from rest_framework.exceptions import AuthenticationFailed, NotFound, APIException

logger = logging.getLogger(__name__)

class FinnhubAPIService:
    """Finnhub APIと連携して会社概要を取得するサービス"""

    def __init__(self, client):
        self.client = client

    def fetch_company_profile(self, symbol: str) -> dict:

        try:
            profile_data = self.client.company_profile2(symbol=symbol)
            if profile_data:
                return profile_data
            raise NotFound(f"No data found for symbol: {symbol}")
        
        except (AuthenticationFailed, NotFound, TimeoutError) as e:
            logger.error(f"Error fetching data from Finnhub: {e}")
            raise e
            
        except Exception as e:
            logger.error(f"Unexpected error fetching data from Finnhub: {e}")
            raise APIException(f"An unexpected error occurred: {e}")
