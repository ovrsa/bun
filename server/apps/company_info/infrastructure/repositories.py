from django.core.cache import cache
from django.db import transaction
from ..domain.repositories import CompanyProfileRepository
from ..models import TickerReference, CompanyProfile, StockPrice, CompanyFinancials

import logging

logger = logging.getLogger(__name__)

class CompanyProfileRepositoryImpl(CompanyProfileRepository):
    """Use ORM to get and save company profile data"""
    
    CACHE_KEY_TEMPLATE = "company_profile_{ticker}"

    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """Select company profile data for the specified ticker"""
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        company_profile = cache.get(cache_key)

        if company_profile:
            return company_profile

        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            company_profile = CompanyProfile.objects.get(ticker=ticker_ref)
            cache.set(cache_key, company_profile, timeout=3600)
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
        cache.set(cache_key, company_profile, timeout=3600)

        return company_profile


class StockPriceRepositoryImpl:
    """Use ORM to get and save stock price data"""

    def get_by_ticker(self, ticker: str) -> list:
        """Select stock price data for the specified ticker"""
        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            stock_prices = StockPrice.objects.filter(ticker=ticker_ref)
            return stock_prices
        except TickerReference.DoesNotExist:
            logger.error(f"TickerReference not found for ticker: {ticker}")
            return None

    def save(self, ticker: str, stock_data: list) -> list:
        """Save stock price data"""
        ticker_ref = TickerReference.objects.get(ticker=ticker)

        stock_price_objects = [
            StockPrice(
                ticker=ticker_ref,
                date=data['date'],
                close=data['close'],
                high=data['high'],
                low=data['low'],
                moving_average_20=data['moving_average_20'],
                moving_average_50=data['moving_average_50'],
                moving_average_200=data['moving_average_200'],
                rsi=data['rsi'],
                volume=data['volume']
            )
            for data in stock_data
        ]

        with transaction.atomic():
            StockPrice.objects.bulk_create(stock_price_objects, ignore_conflicts=True)

        return stock_price_objects


class CompanyFinancialsRepositoryImpl:
    """Use ORM to get and save company financial data"""

    def get_by_ticker(self, ticker: str) -> list:
        """Select financial data for the specified ticker"""
        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            financials = CompanyFinancials.objects.filter(ticker=ticker_ref)
            return financials
        except TickerReference.DoesNotExist:
            logger.error(f"Ticker reference not found for ticker: {ticker}")
            return None

    def save(self, ticker: str, financial_data: dict) -> list:
        """Save financial data"""
        ticker_ref = TickerReference.objects.get(ticker=ticker)

        financial_objects = []
        for data in financial_data.values():
            financials, created = CompanyFinancials.objects.update_or_create(
                ticker=ticker_ref,
                fiscal_year=data['fiscal_year'],
                defaults={
                    'fiscal_year': data['fiscal_year'],
                    'total_revenue': data['total_revenue'],
                    'normalized_ebitda': data['normalized_ebitda'],
                    'stockholders_equity': data['stockholders_equity'],
                    'free_cash_flow': data['free_cash_flow'],
                    'capital_expenditures': data['capital_expenditures'],
                    'total_assets': data['total_assets'],
                    'total_liabilities': data['total_liabilities'],
                    'gross_profit': data['gross_profit'],
                    'net_income_loss': data['net_income_loss'],
                    'net_debt': data['net_debt'],
                    'enterprise_value': data['enterprise_value'],
                    'ebitda_margin': data['ebitda_margin'],
                    'net_debt_to_ebitda': data['net_debt_to_ebitda'],
                    'roa': data['roa'],
                    'roe': data['roe'],
                    'debt_to_equity': data['debt_to_equity'],
                    'operating_margin': data['operating_margin'],
                    'cash_from_operations': data['cash_from_operations'],
                    'change_in_working_capital': data['change_in_working_capital'],
                }
            )
            financial_objects.append(financials)

        return financial_objects
