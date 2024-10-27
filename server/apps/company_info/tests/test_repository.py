import time
from django.test import TestCase
from django.core.cache import cache
from unittest.mock import patch
from ..models import TickerReference, CompanyProfile
from ..infrastructure.repositories import CompanyProfileRepositoryImpl

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
        CompanyProfile.objects.create(ticker=self.ticker_ref, **self.profile_data)

    @patch('django.core.cache.cache.get')
    def test_cache_hit(self, mock_cache_get):
        """キャッシュが存在するシナリオの確認"""
        mock_cache_get.return_value = self.profile_data

        cached_data = self.repository.get_from_cache('company_profile_AAPL')
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data['company_name'], 'Apple Inc.')

    @patch('django.core.cache.cache.get', return_value=None)
    @patch('django.core.cache.cache.set')
    def test_cache_miss(self, mock_cache_set, mock_cache_get):
        """キャッシュミス後にDBからデータが取得されることの確認"""
        company_profile = self.repository.get_by_ticker('AAPL')

        self.assertIsNotNone(company_profile, "キャッシュミス後にDBからデータが取得できません")
        self.assertEqual(company_profile.company_name, 'Apple Inc.')
        mock_cache_set.assert_called_once()

    def test_cache_expiry(self):
        """キャッシュが1時間後にリセットされることを確認する"""
        cache_key = "company_profile_AAPL"
        
        # キャッシュにデータをセット
        self.repository.save(self.profile_data, self.ticker_ref)
        cached_data = self.repository.get_from_cache(cache_key)
        
        # データがキャッシュされていることを確認
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data.company_name, 'Apple Inc.')

        # 時間を1時間進める（3600秒）
        with patch('time.time', return_value=time.time() + 3601):
            expired_data = self.repository.get_from_cache(cache_key)
            self.assertIsNone(expired_data, "キャッシュが期限切れになっていません")
