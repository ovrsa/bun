from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.db import transaction
import numpy as np

from .base_repository import CacheRepository
from ..domain import repositories
from ..models import TickerReference, CompanyProfile, StockPrice, CompanyFinancials

from ..infrastructure import external_services
from ..domain import services

import logging

logger = logging.getLogger(__name__)

class CompanyProfileRepositoryImpl(CacheRepository, repositories.CompanyProfileRepository):
    """Use ORM to get and save company profile data"""

    CACHE_KEY_TEMPLATE = "company_profile_{ticker}"
    DATA_EXPIRATION = timedelta(hours=24)

    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """Select company profile data for the specified ticker"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        company_profile = self.get_from_cache(cache_key)

        if company_profile:
            return company_profile

        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            company_profile = CompanyProfile.objects.get(ticker=ticker_ref)

            # If the data is older than 24 hours, fetch new data
            if company_profile.updated_at < timezone.now() - self.DATA_EXPIRATION:
                new_data = self.fetch_new_data(ticker_ref)
                company_profile = self.save(new_data, ticker_ref)
        
            self.set_to_cache(cache_key, company_profile)
            return company_profile

        except (TickerReference.DoesNotExist, CompanyProfile.DoesNotExist) as e:
            logger.error(f"No profile found for ticker {ticker}: {str(e)}")
            return None

    def fetch_new_data(self, ticker_ref):
        """Fetch new company profile data from the external API"""
        fetcher = external_services.YFinanceCompanyProfileFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
        processed_data = services.CompanyProfileProcessor.process_raw_data(raw_data)
        return processed_data

    def save(self, company_profile_data: dict, ticker_ref: TickerReference) -> CompanyProfile:
        """Save company profile data"""

        company_profile, created = CompanyProfile.objects.update_or_create(
            ticker=ticker_ref,
            defaults={
                'company_name': company_profile_data.get('company_name', None),
                'exchange': company_profile_data.get('exchange', None),
                'market_category': company_profile_data.get('market_category', None),
                'industry': company_profile_data.get('industry', None),
                'sector': company_profile_data.get('sector', None),
                'address': company_profile_data.get('address', None),
                'phone_number': company_profile_data.get('phone_number', None),
                'website': company_profile_data.get('website', None),
                'founding_year': company_profile_data.get('founding_year', None),
                'employee_count': company_profile_data.get('employee_count', None),
                'outstanding_shares': company_profile_data.get('outstanding_shares', None),
                'market_capitalization': company_profile_data.get('market_capitalization', None),
                'average_trading_volume_10d': company_profile_data.get('average_trading_volume_10d', None),
                'business_description': company_profile_data.get('business_description', None),
            }
        )

        company_profile = CompanyProfile.objects.get(ticker=ticker_ref)
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker_ref.ticker)
        self.set_to_cache(cache_key, company_profile)

        return company_profile


class StockPriceRepositoryImpl(CacheRepository, repositories.StockPriceRepository):
    """Use ORM to get and save stock price data"""

    CACHE_KEY_TEMPLATE = "stock_price_{ticker}"
    DATA_EXPIRATION = timedelta(hours=24)

    def get_by_ticker(self, ticker: str) -> list:
        """Get stock prices by ticker with cache and update logic"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        stock_prices = self.get_from_cache(cache_key)

        if stock_prices:
            return stock_prices

        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            stock_prices_qs = StockPrice.objects.filter(ticker=ticker_ref)
            stock_prices = list(stock_prices_qs.values())

            # If the data is older than 24 hours, fetch new data
            if stock_prices and stock_prices_qs.latest('updated_at').updated_at < timezone.now() - self.DATA_EXPIRATION:
                new_data = self.fetch_new_data(ticker)
                stock_prices = self.save(ticker, new_data)

            # If there is no data in the database, fetch new data
            elif not stock_prices:
                new_data = self.fetch_new_data(ticker)
                stock_prices = self.save(ticker, new_data)

            # Update cache
            self.set_to_cache(cache_key, stock_prices)
            return stock_prices

        except TickerReference.DoesNotExist as e:
            logger.error(f"No stock prices found for ticker {ticker}: {str(e)}")
            return None

    def fetch_new_data(self, ticker: str):
        """Fetch new stock price data from the external API"""
        fetcher = external_services.YFinanceStockPriceFetcher()
        raw_data = fetcher.fetch(ticker)
        if raw_data.empty:
            logger.warning(f"No data fetched for ticker {ticker}")
            return []
        processed_data = services.StockPriceProcessor.process_raw_data(raw_data)
        return processed_data

    def save(self, ticker: str, stock_data: list) -> list:
        """Save and cache stock prices"""
        ticker_ref = TickerReference.objects.get(ticker=ticker)
        stock_price_objects = [
            StockPrice(ticker=ticker_ref, **data) for data in stock_data
        ]

        with transaction.atomic():
            StockPrice.objects.bulk_create(stock_price_objects, ignore_conflicts=True)

        saved_stock_prices = list(StockPrice.objects.filter(ticker=ticker_ref).values())

        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        self.set_to_cache(cache_key, saved_stock_prices)
        return saved_stock_prices


class CompanyFinancialsRepositoryImpl(CacheRepository, repositories.CompanyFinancialsRepository):
    """Use ORM to get and save company financial data"""

    CACHE_KEY_TEMPLATE = "company_financials_{ticker}"
    DATA_EXPIRATION = timedelta(hours=24)

    def get_by_ticker(self, ticker: str) -> list:
        """Get financial data by ticker with cache and update logic"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        financials = self.get_from_cache(cache_key)

        if financials:
            return financials

        try:
            # fetch for database
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            financials_qs = CompanyFinancials.objects.filter(ticker=ticker_ref)
            financials = list(financials_qs.values())

            # If the data is older than 24 hours, fetch new data
            if financials and financials_qs.latest('updated_at').updated_at < timezone.now() - self.DATA_EXPIRATION:
                new_data = self.fetch_new_data(ticker_ref)
                financials = self.save(ticker, new_data)

            # If there is no data in the database, fetch new data
            elif not financials:
                new_data = self.fetch_new_data(ticker_ref)
                financials = self.save(ticker, new_data)

            # Update cache
            self.set_to_cache(cache_key, financials)
            return financials

        except TickerReference.DoesNotExist as e:
            logger.error(f"No financial data found for ticker {ticker}: {str(e)}")
            return None

    def fetch_new_data(self, ticker_ref):
        """Fetch new financial data from the external API"""
        fetcher = external_services.YFinanceCompanyFinancialsFetcher()
        raw_data = fetcher.fetch(ticker_ref.ticker)
        if not raw_data:
            return []
        processed_data = services.FinancialDataProcessor.process_financial_data(
            raw_data['balance_sheet'],
            raw_data['cashflow'],
            raw_data['income_stmt']
        )
        return processed_data

    def _sanitize_value(self, value):
        """Convert NaN to None to prevent database errors."""
        if isinstance(value, float) and np.isnan(value):
            return None
        return value

    def save(self, ticker: str, financial_data: dict) -> list:
        """Save financial data and update cache."""
        ticker_ref = TickerReference.objects.get(ticker=ticker)

        financial_objects = []
        for data in financial_data.values():
            sanitized_data = {k: self._sanitize_value(v) for k, v in data.items()}

            financial, created = CompanyFinancials.objects.update_or_create(
                ticker=ticker_ref,
                fiscal_year=sanitized_data['fiscal_year'],
                defaults=sanitized_data,
            )
            financial_objects.append(financial)

        # Update cache
        saved_financials = list(CompanyFinancials.objects.filter(ticker=ticker_ref).values())
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        self.set_to_cache(cache_key, saved_financials)

        return saved_financials