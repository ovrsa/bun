import unittest
from unittest.mock import MagicMock
from apps.company_analytics.Application.use_cases import GetStockPriceUseCase
from apps.company_analytics.Domain.models import TickerReference, StockPrice


class TestGetStockPriceUseCase(unittest.TestCase):
    """ GetStockPriceUseCaseのテストクラス """

    def setUp(self):
        self.mock_fetcher = MagicMock()
        self.use_case = GetStockPriceUseCase(fetcher=self.mock_fetcher)

    def test_execute_existing_stock_prices(self):
        """ 既存の株価情報がある場合のテスト """
        ticker = "AAPL"
        TickerReference.objects.get_or_create = MagicMock(
            return_value=(TickerReference(ticker=ticker), False)
        )
        StockPrice.objects.filter = MagicMock(
            return_value=MagicMock(exists=MagicMock(return_value=True))
        )
        result = self.use_case.execute(ticker)
        self.assertIsNotNone(result)

    def test_execute_missing_stock_prices(self):
        """ 株価情報がない場合のテスト """
        ticker = "AAPL"
        TickerReference.objects.get_or_create = MagicMock(
            return_value=(TickerReference(ticker=ticker), False)
        )
        StockPrice.objects.filter = MagicMock(
            return_value=MagicMock(exists=MagicMock(return_value=False))
        )
        self.mock_fetcher.fetch = MagicMock(return_value=[
            {
                "Date": "2024-01-01",
                "Close": 150,
                "High": 155,
                "Low": 145,
                "Volume": 1000
            }
        ])
        from apps.company_analytics.Domain.services import StockPriceProcessor
        StockPriceProcessor.process_raw_data = MagicMock(return_value=[
            {
                "date": "2024-01-01",
                "close": 150,
                "high": 155,
                "low": 145,
                "volume": 1000,
            }
        ])
        StockPrice.objects.update_or_create = MagicMock()
        result = self.use_case.execute(ticker)
        self.assertTrue(result)

    def test_update_stock_prices(self):
        """ 株価情報の更新テスト """

        ticker_ref = MagicMock(ticker="AAPL")
        self.mock_fetcher.fetch = MagicMock(return_value=[
            {
                "Date": "2024-01-01",
                "Close": 150, "High": 155,
                "Low": 145,
                "Volume": 1000
            }
        ])
        from apps.company_analytics.Domain.services import StockPriceProcessor
        StockPriceProcessor.process_raw_data = MagicMock(return_value=[
            {
                "date": "2024-01-01",
                "close": 150,
                "high": 155,
                "low": 145,
                "volume": 1000,
            }
        ])
        mock_stock_price = MagicMock()
        StockPrice.objects.update_or_create = MagicMock(return_value=(
            mock_stock_price,
            True
            )
        )

        result = self.use_case._update_stock_prices(ticker_ref)

        # モックが正しいパラメータで呼び出されたことを確認
        StockPrice.objects.update_or_create.assert_called_with(
            ticker=ticker_ref,
            date="2024-01-01",
            defaults={
                "date": "2024-01-01",
                "close": 150,
                "high": 155,
                "low": 145,
                "volume": 1000,
            }
        )
        # 結果の検証
        assert result == [mock_stock_price]


if __name__ == "__main__":
    unittest.main()
