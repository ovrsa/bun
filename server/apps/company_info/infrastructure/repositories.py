from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.db import transaction
import numpy as np


from .base_repository import CacheRepository
from ..domain import repositories
from ..models import TickerReference, CompanyProfile, StockPrice, CompanyFinancials

import logging

logger = logging.getLogger(__name__)

class CompanyProfileRepositoryImpl(CacheRepository, repositories.CompanyProfileRepository):
    """Use ORM to get and save company profile data"""

    CACHE_KEY_TEMPLATE = "company_profile_{ticker}"

    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """Select company profile data for the specified ticker"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        company_profile = self.get_from_cache(cache_key)

        if company_profile:
            return company_profile

        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            company_profile = CompanyProfile.objects.get(ticker=ticker_ref)
            self.set_to_cache(cache_key, company_profile)
            return company_profile
        except (TickerReference.DoesNotExist, CompanyProfile.DoesNotExist):
            logger.error(f"CompanyProfile not found for ticker: {ticker}")
            return None

    def save(self, company_profile_data: dict, ticker_ref: TickerReference) -> CompanyProfile:
        """Save company profile data"""
        company_profile, created = CompanyProfile.objects.update_or_create(
            ticker=ticker_ref,
            defaults={
                'company_name': company_profile_data.get('company_name', ''),
                'exchange': company_profile_data.get('exchange', ''),
                'market_category': company_profile_data.get('market_category', ''),
                'industry': company_profile_data.get('industry', ''),
                'sector': company_profile_data.get('sector', ''),
                'address': company_profile_data.get('address', ''),
                'phone_number': company_profile_data.get('phone_number', ''),
                'website': company_profile_data.get('website', ''),
                'founding_year': company_profile_data.get('founding_year', 0),
                'employee_count': company_profile_data.get('employee_count', 0),
                'outstanding_shares': company_profile_data.get('outstanding_shares', 0),
                'market_capitalization': company_profile_data.get('market_capitalization', 0.0),
                'average_trading_volume_10d': company_profile_data.get('average_trading_volume_10d', 0),
                'business_description': company_profile_data.get('business_description', ''),
            }
        )

        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker_ref.ticker)
        self.set_to_cache(cache_key, company_profile)

        return company_profile


class StockPriceRepositoryImpl(CacheRepository, repositories.StockPriceRepository):
    CACHE_KEY_TEMPLATE = "stock_price_{ticker}"
    DATA_EXPIRATION = timedelta(hours=24)

    def get_by_ticker(self, ticker: str) -> list:
        """Get stock prices by ticker with cache and update logic"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        stock_prices = self.get_from_cache(cache_key)

        if stock_prices:
            return stock_prices

        ticker_ref = TickerReference.objects.get(ticker=ticker)
        stock_prices = StockPrice.objects.filter(ticker=ticker_ref)

        # 更新日時の確認：データが24時間以上経過していたら再取得
        if stock_prices and stock_prices.latest('updated_at').updated_at < timezone.now() - self.DATA_EXPIRATION:
            return None  # 古いデータとして扱い、外部APIで再取得させる

        self.set_to_cache(cache_key, list(stock_prices.values()))
        return stock_prices

    def save(self, ticker: str, stock_data: list) -> list:
        """Save and cache stock prices"""
        ticker_ref = TickerReference.objects.get(ticker=ticker)
        stock_price_objects = [
            StockPrice(ticker=ticker_ref, **data) for data in stock_data
        ]

        with transaction.atomic():
            StockPrice.objects.bulk_create(stock_price_objects, ignore_conflicts=True)

        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        self.set_to_cache(cache_key, stock_data)
        return stock_price_objects



class CompanyFinancialsRepositoryImpl(CacheRepository, repositories.CompanyFinancialsRepository):
    CACHE_KEY_TEMPLATE = "company_financials_{ticker}"
    DATA_EXPIRATION = timedelta(hours=24)

    def get_by_ticker(self, ticker: str) -> list:
        """Get financial data by ticker with cache and update logic."""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        financials = self.get_from_cache(cache_key)

        if financials:
            return financials

        ticker_ref = TickerReference.objects.get(ticker=ticker)
        financials = CompanyFinancials.objects.filter(ticker=ticker_ref)

        if financials and financials.latest('updated_at').updated_at < timezone.now() - self.DATA_EXPIRATION:
            return None

        self.set_to_cache(cache_key, list(financials.values()))
        return financials

    def _sanitize_value(self, value):
        """Convert NaN to None to prevent MySQL errors."""
        if isinstance(value, float) and np.isnan(value):
            return None
        return value

    def save(self, ticker: str, financial_data: dict) -> list:
        """Save financial data and update cache."""
        ticker_ref = TickerReference.objects.get(ticker=ticker)

        financial_objects = []
        for data in financial_data.values():
            sanitized_data = {k: self._sanitize_value(v) for k, v in data.items()}

            financials, created = CompanyFinancials.objects.update_or_create(
                ticker=ticker_ref,
                fiscal_year=sanitized_data['fiscal_year'],
                defaults=sanitized_data,
            )
            financial_objects.append(financials)

        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        self.set_to_cache(cache_key, list(financial_objects))
        return financial_objects
