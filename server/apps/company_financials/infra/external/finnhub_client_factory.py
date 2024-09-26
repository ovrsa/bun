import finnhub
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class FinnhubClientFactory:
    
    def create_client(self):
        try:
            return finnhub.Client(api_key=settings.FINNHUB_API_KEY)
        
        except Exception as e:
            logger.error(f"Failed to initialize Finnhub client: {e}")
            raise Exception("Failed to initialize Finnhub client.")
