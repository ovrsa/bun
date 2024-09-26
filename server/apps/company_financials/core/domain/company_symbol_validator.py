from rest_framework.exceptions import  NotFound

class CompanySymbolValidator:

    @staticmethod
    def validate(symbol: str) -> None:
        if not symbol:
            raise NotFound("Symbol is required")