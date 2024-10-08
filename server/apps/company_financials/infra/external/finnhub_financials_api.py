import logging
from rest_framework.exceptions import APIException, NotFound

logger = logging.getLogger(__name__)


class FinnhubFinancialsAPI:

    def __init__(self, client):
        self.client = client

    def fetch_company_financials(self, symbol: str) -> dict:
        try:
            financials_data = self.client.financials_reported(symbol=symbol)
            if financials_data:
                return financials_data
            raise NotFound(f"No data found for symbol: {symbol}")
        except Exception as e:
            logger.error(f"Error fetching data from Finnhub: {e}")
            raise APIException(f"An error occurred: {e}")
