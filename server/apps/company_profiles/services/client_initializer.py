import finnhub
from django.conf import settings
import logging
from rest_framework.exceptions import APIException

logger = logging.getLogger('app')


class ClientInitializer:

    def __init__(self):
        self.client = self.initialize_client()

    def initialize_client(self):
        try:
            return finnhub.Client(api_key=settings.FINNHUB_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Finnhub client: {e}")
            raise APIException("Failed to initialize Finnhub client.")
