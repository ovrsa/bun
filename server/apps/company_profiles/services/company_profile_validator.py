class CompanyProfileValidator:

    @staticmethod
    def validate_symbol(symbol: str) -> None:
        if not symbol:
            raise ValueError("Symbol is required")

    @staticmethod
    def validate_profile_data(data: dict) -> None:
        if not data.get('ticker') or not data.get('name'):
            raise ValueError("Ticker and Company Name are required")
