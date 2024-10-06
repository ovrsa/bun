from django.core.cache import cache
from ..models import CompanyProfile
from ..domain.repositories import CompanyProfileRepository

class DjangoCompanyProfileRepository(CompanyProfileRepository):
    """ DjangoのORMを使って企業情報を取得・保存するためのリポジトリ """
    
    CACHE_KEY_TEMPLATE = "company_profile_{ticker}"

    def get_by_ticker(self, ticker: str) -> CompanyProfile:
        """ 銘柄コードから企業情報を取得する """
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=ticker)
        company_profile = cache.get(cache_key)
        
        if company_profile:
            print(f"Cache hit for {ticker}")
            return company_profile

        try:
            company_profile = CompanyProfile.objects.get(ticker=ticker)
            cache.set(cache_key, company_profile, timeout=3600)
            return company_profile
        except CompanyProfile.DoesNotExist:
            return None


    def save(self, company_profile: CompanyProfile) -> None:
        """ 企業情報を保存する """
        obj, _ = CompanyProfile.objects.update_or_create(
            ticker=company_profile.ticker,
            defaults={
                'company_name': company_profile.company_name,
                'exchange': company_profile.exchange,
                'market_category': company_profile.market_category,
                'industry': company_profile.industry,
                'sector': company_profile.sector,
                'address': company_profile.address,
                'phone_number': company_profile.phone_number,
                'website': company_profile.website,
                'founding_year': company_profile.founding_year,
                'employee_count': company_profile.employee_count,
                'outstanding_shares': company_profile.outstanding_shares,
                'market_capitalization': company_profile.market_capitalization,
                'average_trading_volume_10d': company_profile.average_trading_volume_10d,
                'business_description': company_profile.business_description,
            }
        )

        # データベース保存後、キャッシュも更新
        cache_key = self.CACHE_KEY_TEMPLATE.format(ticker=company_profile.ticker)
        cache.set(cache_key, company_profile, timeout=3600)