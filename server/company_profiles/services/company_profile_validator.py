class CompanyProfileValidator:
    """会社概要関連データのバリデートを行う"""

    @staticmethod
    def validate_symbol(symbol: str) -> None:
        """
        指定されたシンボルが空または None ではないことを検証

        Args:
            symbol (str): 検証する銘柄記号

        Raises:
            ValueError: シンボルが空または None の場合
        """
        if not symbol:
            raise ValueError("Symbol is required")

    @staticmethod
    def validate_profile_data(data: dict) -> None:
        """
        プロファイル データに必須フィールド「ティッカー」と「名前」が含まれていることを検証

        Args:
            data (dict): 検証するプロファイル データ

        Raises:
            データに「ティッカー」または「名前」が欠落している場合
        """
        if not data.get('ticker') or not data.get('name'):
            raise ValueError("Ticker and Company Name are required")
