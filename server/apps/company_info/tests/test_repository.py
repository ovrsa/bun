from django.utils import timezone
from django.test import TestCase
from django.core.cache import cache

from datetime import timedelta
from unittest.mock import patch

import pandas as pd

from ..models import TickerReference, StockPrice, CompanyProfile, CompanyFinancials
from ..infrastructure.repositories import (
    CompanyProfileRepositoryImpl,
    StockPriceRepositoryImpl,
    CompanyFinancialsRepositoryImpl,
)
from ..infrastructure.external_services import (
    YFinanceCompanyProfileFetcher,
    YFinanceStockPriceFetcher,
    YFinanceCompanyFinancialsFetcher,
)

class CompanyProfileCacheTest(TestCase):
    def setUp(self):
        """テストデータのセットアップ"""
        self.ticker_ref = TickerReference.objects.create(ticker="AAPL")
        self.profile_data = {
            'company_name': 'Apple Inc.',
            'exchange': 'NASDAQ',
            'market_category': 'Technology',
            'industry': 'Consumer Electronics',
            'sector': 'Technology',
            'address': 'One Apple Park Way, Cupertino, CA',
            'phone_number': '123-456-7890',
            'website': 'https://www.apple.com',
            'founding_year': 1976,
            'employee_count': 154000,
            'market_capitalization': 2500000000000,
        }
        self.repository = CompanyProfileRepositoryImpl()

        # テストDBにデータを保存
        self.company_profile = CompanyProfile.objects.create(
            ticker=self.ticker_ref, **self.profile_data
        )

        # キャッシュにもセット
        self.repository.set_to_cache('company_profile_AAPL', self.company_profile)

    @patch('django.core.cache.cache.get')
    def test_cache_hit(self, mock_cache_get):
        """キャッシュが存在するシナリオの確認"""
        mock_cache_get.return_value = self.company_profile

        cached_data = self.repository.get_from_cache('company_profile_AAPL')
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data.company_name, 'Apple Inc.')

    @patch('django.core.cache.cache.get', return_value=None)
    @patch('django.core.cache.cache.set')
    def test_cache_miss(self, mock_cache_set, mock_cache_get):
        """キャッシュミス後にDBからデータが取得されることの確認"""
        company_profile = self.repository.get_by_ticker('AAPL')

        self.assertIsNotNone(company_profile)
        self.assertEqual(company_profile.company_name, 'Apple Inc.')
        mock_cache_set.assert_called_once()

    @patch.object(YFinanceCompanyProfileFetcher, 'fetch', return_value={
        'longName': 'Apple Inc. Updated',
        'exchange': 'NASDAQ',
        'quoteType': 'Technology',
        'industry': 'Consumer Electronics',
        'sector': 'Technology',
        'address1': 'One Apple Park Way',
        'city': 'Cupertino',
        'state': 'CA',
        'zip': '95014',
        'country': 'USA',
        'phone': '123-456-7890',
        'website': 'https://www.apple.com',
        'companyOfficers': [{'yearBorn': 1976}],
        'fullTimeEmployees': 160000,
        'sharesOutstanding': 100000,
        'marketCap': 2600000000000,
        'averageVolume10days': 10000,
        'longBusinessSummary': 'Technology company.',
    })
    def test_data_refresh_after_24_hours(self, mock_fetch):
        """24時間後に外部APIから再取得し、DBが上書きされることの確認"""
        
        # 時間を24時間以上前に設定
        past_time = timezone.now() - timedelta(hours=24, seconds=1)
        CompanyProfile.objects.filter(ticker=self.ticker_ref).update(updated_at=past_time)

        # キャッシュをクリア
        cache.clear()
        self.assertIsNone(self.repository.get_from_cache('company_profile_AAPL'))

        # データ取得と保存を確認
        refreshed_profile = self.repository.get_by_ticker('AAPL')
        print(f"Refreshed Profile: {refreshed_profile}")

        # 期待するデータかを確認
        self.assertIsNotNone(refreshed_profile)
        self.assertEqual(refreshed_profile.company_name, 'Apple Inc. Updated')
        self.assertEqual(refreshed_profile.employee_count, 160000)

        # fetch が1回だけ呼ばれたことを確認
        mock_fetch.assert_called_once()


class StockPriceCacheTest(TestCase):
    def setUp(self):
        """テストデータのセットアップ"""
        self.ticker_ref = TickerReference.objects.create(ticker="AAPL")
        self.stock_data = [
            {
                "date": "2024-02-12",
                "close": 837.0042724609375,
                "high": 845.4730217968998,
                "low": 832.5336012768116,
                "moving_average_20": 813.0122467041016,
                "moving_average_50": 801.3469006347656,
                "moving_average_200": 754.9236840820313,
                "rsi": 70.85572724644884,
                "volume": 434400,
            },
            {
                "date": "2024-02-13",
                "close": 819.9684448242188,
                "high": 824.7640954435037,
                "low": 813.6070404227181,
                "moving_average_20": 813.6798950195313,
                "moving_average_50": 801.6949047851563,
                "moving_average_200": 755.5316491699218,
                "rsi": 63.79845453254472,
                "volume": 448700,
            },
        ]
        self.repository = StockPriceRepositoryImpl()

        # テストDBにデータを保存
        for data in self.stock_data:
            StockPrice.objects.create(ticker=self.ticker_ref, **data)

        # キャッシュにもセット
        self.repository.set_to_cache('stock_price_AAPL', self.stock_data)

    @patch('django.core.cache.cache.get')
    def test_cache_hit(self, mock_cache_get):
        """キャッシュが存在するシナリオの確認"""
        mock_cache_get.return_value = self.stock_data

        cached_data = self.repository.get_from_cache('stock_price_AAPL')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]["close"], 837.0042724609375)

    @patch('django.core.cache.cache.get', return_value=None)
    @patch('django.core.cache.cache.set')
    def test_cache_miss(self, mock_cache_set, mock_cache_get):
        """キャッシュミス後にDBからデータが取得されることの確認"""
        stock_prices = self.repository.get_by_ticker('AAPL')

        self.assertIsNotNone(stock_prices)
        self.assertEqual(len(stock_prices), 2)
        self.assertEqual(stock_prices[0]["close"], 837.0042724609375)
        mock_cache_set.assert_called_once()

    @patch.object(YFinanceStockPriceFetcher, 'fetch')
    def test_data_refresh_after_24_hours(self, mock_fetch):
        """24時間後に外部APIから再取得し、DBが上書きされることの確認"""

        # モックされたAPIの返却データ
        mock_fetch.return_value = pd.DataFrame({
            'Date': [pd.Timestamp('2024-02-14')],
            'Close': [830.0],
            'High': [835.0],
            'Low': [820.0],
            'Volume': [460000],
        })

        # `updated_at` を24時間以上前に設定
        past_time = timezone.now() - timedelta(hours=24, seconds=1)
        StockPrice.objects.filter(ticker=self.ticker_ref).update(updated_at=past_time)

        # キャッシュをクリア
        cache.clear()
        self.assertIsNone(self.repository.get_from_cache('stock_price_AAPL'))

        # データ取得と検証
        refreshed_data = self.repository.get_by_ticker('AAPL')
        print(f"Refreshed Data: {refreshed_data}")

        # データが3件になっていることを確認
        self.assertEqual(len(refreshed_data), 3)  # 期待するデータ件数に修正
        self.assertEqual(refreshed_data[-1]["close"], 830.0)
        self.assertEqual(refreshed_data[-1]["volume"], 460000)

        # fetch が1回だけ呼ばれたことを確認
        mock_fetch.assert_called_once_with('AAPL')
        

class CompanyFinancialsCacheTest(TestCase):
    def setUp(self):
        """テストデータのセットアップ"""
        self.ticker_ref = TickerReference.objects.create(ticker="AAPL")
        self.financial_data = [
            {
                "fiscal_year": 2020,
                "total_revenue": 274515000000.0,
                "normalized_ebitda": 81474000000.0,
                "stockholders_equity": 65339000000.0,
                "free_cash_flow": 73865000000.0,
                "capital_expenditures": -7309000000.0,
                "total_assets": 323888000000.0,
                "total_liabilities": 258549000000.0,
                "gross_profit": 0.382,
                "net_income_loss": 57411000000.0,
                "net_debt": 9790000000.0,
                "enterprise_value": 2046293180416.0,
                "ebitda_margin": 0.2969,
                "net_debt_to_ebitda": 0.1202,
                "roa": 0.1773,
                "roe": 0.2621,
                "debt_to_equity": 1.191,
                "operating_margin": 0.241,
                "cash_from_operations": 80074000000.0,
                "change_in_working_capital": 1325000000.0,
            },
            {
                "fiscal_year": 2021,
                "total_revenue": 365817000000.0,
                "normalized_ebitda": 120233000000.0,
                "stockholders_equity": 63090000000.0,
                "free_cash_flow": 93865000000.0,
                "capital_expenditures": -11085000000.0,
                "total_assets": 351002000000.0,
                "total_liabilities": 287912000000.0,
                "gross_profit": 0.417,
                "net_income_loss": 94680000000.0,
                "net_debt": 6600000000.0,
                "enterprise_value": 2246293180416.0,
                "ebitda_margin": 0.3286,
                "net_debt_to_ebitda": 0.0549,
                "roa": 0.2697,
                "roe": 0.4285,
                "debt_to_equity": 1.385,
                "operating_margin": 0.297,
                "cash_from_operations": 104038000000.0,
                "change_in_working_capital": -5988000000.0,
            },
        ]
        self.repository = CompanyFinancialsRepositoryImpl()

        # テストDBにデータを保存
        for data in self.financial_data:
            CompanyFinancials.objects.create(ticker=self.ticker_ref, **data)

        # キャッシュにもセット
        self.repository.set_to_cache('company_financials_AAPL', self.financial_data)

    @patch('django.core.cache.cache.get')
    def test_cache_hit(self, mock_cache_get):
        """キャッシュが存在するシナリオの確認"""
        mock_cache_get.return_value = self.financial_data

        cached_data = self.repository.get_from_cache('company_financials_AAPL')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]["fiscal_year"], 2020)
        self.assertEqual(cached_data[0]["total_revenue"], 274515000000.0)

    @patch('django.core.cache.cache.get', return_value=None)
    @patch('django.core.cache.cache.set')
    def test_cache_miss(self, mock_cache_set, mock_cache_get):
        """キャッシュミス後にDBからデータが取得されることの確認"""
        financials = self.repository.get_by_ticker('AAPL')

        self.assertIsNotNone(financials)
        self.assertEqual(len(financials), 2)
        self.assertEqual(financials[0]["fiscal_year"], 2020)
        self.assertEqual(financials[0]["total_revenue"], 274515000000.0)
        mock_cache_set.assert_called_once()

    @patch.object(YFinanceCompanyFinancialsFetcher, 'fetch', return_value={
        'info': {
            'totalRevenue': 400000000000.0,
            'ebitda': 130000000000.0,
            'netIncomeToCommon': 100000000000.0,
            'freeCashflow': 100000000000.0,
            'totalDebt': 120000000000.0,
            'totalCash': 60000000000.0,
            'enterpriseValue': 2500000000000.0,
            'grossMargins': 0.42,
        },
        'balance_sheet': pd.DataFrame({
            pd.Timestamp('2022-09-30'): {
                'Total Assets': 352755000000.0,
                'Total Liabilities Net Minority Interest': 287912000000.0,
                'equity': 64843000000.0,
            }
        }),
        'cashflow': pd.DataFrame({
            pd.Timestamp('2022-09-30'): {
                'Operating Cash Flow': 104000000000.0,
                'Change In Working Capital': -1000000000.0,
                'capital expenditure': -11000000000.0,
            }
        }),
    })
    def test_data_refresh_after_24_hours(self, mock_fetch):
        """24時間後に外部APIから再取得し、DBが上書きされることの確認"""

        # 時間を24時間以上前に設定
        past_time = timezone.now() - timedelta(hours=24, seconds=1)
        CompanyFinancials.objects.filter(ticker=self.ticker_ref).update(updated_at=past_time)

        # キャッシュをクリア
        cache.clear()
        self.assertIsNone(self.repository.get_from_cache('company_financials_AAPL'))

        # データ取得と保存を確認
        refreshed_data = self.repository.get_by_ticker('AAPL')
        print(f"Refreshed Data: {refreshed_data}")

        # データが正しく更新されたか検証
        self.assertIsNotNone(refreshed_data)
        self.assertGreater(len(refreshed_data), 0)
        self.assertEqual(refreshed_data[-1]["fiscal_year"], 2022)
        self.assertEqual(refreshed_data[-1]["total_revenue"], 400000000000.0)
        self.assertEqual(refreshed_data[-1]["net_income_loss"], 100000000000.0)

        # fetch が1回だけ呼ばれたことを確認
        mock_fetch.assert_called_once()