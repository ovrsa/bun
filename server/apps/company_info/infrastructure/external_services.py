from ..application.interfaces import CompanyProfileFetcher
from ..models import CompanyProfile
import yfinance
import math


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


class YFinanceStockPriceFetcher:
    """ YFinanceを使って株価データを取得する """

    def fetch(self, ticker_symbol):
        """
        company_info.models.StockPrice

        Args:
            ticker_symbol (str): 銘柄コード

        Returns:
            List[Dict]: 株価データ
        """
        
        ticker = yfinance.Ticker(ticker_symbol)
        hist = ticker.history(period='3y')
        
        if hist.empty:
            return None

        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        hist['MA200'] = hist['Close'].rolling(window=200).mean()

        # RSIの計算
        delta = hist['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        hist['RSI'] = 100 - (100 / (1 + rs))

        hist.reset_index(inplace=True)
        hist['Date'] = hist['Date'].dt.date

        data = []
        for index, row in hist.iterrows():
            rsi = row['RSI']
            if math.isnan(rsi):
                rsi = None

            ma20 = row['MA20']
            if math.isnan(ma20):
                ma20 = None

            ma50 = row['MA50']
            if math.isnan(ma50):
                ma50 = None

            ma200 = row['MA200']
            if math.isnan(ma200):
                ma200 = None
            
            data.append({
                'date': row['Date'],
                'close': row['Close'],
                'high': row['High'],
                'low': row['Low'],
                'moving_average_20': ma20,
                'moving_average_50': ma50,
                'moving_average_200': ma200,
                'rsi': rsi,
                'volume': row['Volume'],
            })

        return data