from rest_framework.exceptions import  NotFound

class CompanySymbolValidator:
    """会社のシンボルのバリデーションを行う"""

    @staticmethod
    def validate(symbol: str) -> None:
        """
        シンボルのバリデーションを行う

        Args:
            symbol (str): シンボル

        Raises:
            NotFound: シンボルが指定されていない場合
        """
        
        if not symbol:
            raise NotFound("Symbol is required")