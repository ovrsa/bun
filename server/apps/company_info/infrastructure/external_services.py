from ..application.interfaces import CompanyProfileFetcher
from ..models import CompanyProfile
import yfinance

class YFinanceCompanyProfileFetcher(CompanyProfileFetcher):
    """YFinanceを使って企業情報を取得する"""

    def fetch(self, ticker: str) -> CompanyProfile:
        """
        company_info.models.CompanyProfile

        Args:
            ticker (str): 銘柄コード

        Returns:
            company_info.models.CompanyProfile: 企業情報
        """
        
        stock_data = yfinance.Ticker(ticker)
        info = stock_data.info
        return CompanyProfile(
            ticker=info.get('symbol'),
            company_name=info.get('longName'),
            exchange=info.get('exchange'),
            market_category=info.get('quoteType'),
            industry=info.get('industry'),
            sector=info.get('sector'),
            address=f"{info.get('address1')}, {info.get('city')}, {info.get('state')} {info.get('zip')}, {info.get('country')}",
            phone_number=info.get('phone'),
            website=info.get('website'),
            founding_year=info.get('companyOfficers')[0].get('yearBorn'),
            employee_count=info.get('fullTimeEmployees'),
            outstanding_shares=info.get('sharesOutstanding'),
            market_capitalization=info.get('marketCap'),
            average_trading_volume_10d=info.get('averageVolume10days'),
            business_description=info.get('longBusinessSummary'),
        )
