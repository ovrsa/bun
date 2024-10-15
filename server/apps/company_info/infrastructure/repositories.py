from django.core.cache import cache
from ..models import CompanyProfile
from ..models import StockPrice
from ..domain.repositories import CompanyProfileRepository
from ..models import TickerReference, CompanyProfile, StockPrice, CompanyFinancials

class DjangoCompanyProfileRepository(CompanyProfileRepository):
    """DjangoのORMを使って企業情報を取得・保存"""
    
    CACHE_KEY_TEMPLATE = "company_profile_{ticker}"

    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """ 銘柄コードから企業情報を取得する
        
        Args:
            ticker (str): 銘柄コード

        Returns:
            CompanyProfile: 企業情報
        """
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
            return None

    def save(self, company_profile_data, ticker_ref):
        """企業情報をデータベースに保存
        
        Args:
            company_profile_data (dict): 企業情報
            ticker_ref (TickerReference): ティッカーシンボル

        Returns:
            CompanyProfile: 保存された企業情報
        """
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


class DjangoStockPriceRepository:
    """DjangoのORMを使って株価データを取得・保存"""

    def get_by_ticker(self, ticker):
        """指定されたティッカーの株価データを取得する
        
        Args:
            ticker (str): ティッカーシンボル

        Returns:
            List[StockPrice]: 株価データ
        """
        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            return StockPrice.objects.filter(ticker=ticker_ref)
        except TickerReference.DoesNotExist:
            return None

    def save(self, ticker, stock_data):
        """株価データをデータベースに保存する
        
        Args:
            ticker (str): ティッカーシンボル
            stock_data (dict): 株価データ

        Returns:
            List[StockPrice]: 保存された株価データ
        """
        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
        except TickerReference.DoesNotExist:
            return None

        stock_price_objects = []
        for data in stock_data:
            stock_price, created = StockPrice.objects.update_or_create(
                ticker=ticker_ref,
                date=data['date'],
                defaults={
                    'close': data['close'],
                    'high': data['high'],
                    'low': data['low'],
                    'moving_average_20': data['moving_average_20'],
                    'moving_average_50': data['moving_average_50'],
                    'moving_average_200': data['moving_average_200'],
                    'rsi': data['rsi'],
                    'volume': data['volume'],
                }
            )
            stock_price_objects.append(stock_price)
        return stock_price_objects


class DjangoCompanyFinancialsRepository:
    """DjangoのORMを使って企業の財務データを取得・保存"""

    def get_by_ticker(self, ticker: str) -> list:
        """指定されたティッカーの財務データを取得する
        
        Args:
            ticker (str): ティッカーシンボル

        Returns:
            List[CompanyFinancials]: 財務データ
        """
        try:
            ticker_ref = TickerReference.objects.get(ticker=ticker)
            return CompanyFinancials.objects.filter(ticker=ticker_ref)
        except TickerReference.DoesNotExist:
            return None

    def save(self, ticker: str, financial_data: dict) -> list:
        """財務データを保存する
        
        Args:
            ticker (str): ティッカーシンボル
            financial_data (dict): 財務データ

        Returns:
            List[CompanyFinancials]: 保存された財務データ
        """
        try:
            # TickerReference が存在するか確認
            ticker_ref = TickerReference.objects.get(ticker=ticker)
        except TickerReference.DoesNotExist:
            return None

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