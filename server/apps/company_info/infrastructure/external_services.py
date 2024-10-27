from ..application.interfaces import CompanyProfileFetcher
import requests
import yfinance
import pandas

class YFinanceCompanyProfileFetcher(CompanyProfileFetcher):
    """Using YFinance to fetch company profile data"""

    def fetch(self, ticker: str) -> dict:
        """

        Fetch company profile data from YFinance

        Args:
            ticker (str): Stock ticker

        Returns:
            dict: Company profile data

        """
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        session.get('https://finance.yahoo.com', timeout=5)
        stock_data = yfinance.Ticker(ticker, session=session)

        info = stock_data.info

        if not info:
            return None

        return info


class YFinanceStockPriceFetcher:
    """Using YFinance to fetch stock price data"""

    def fetch(self, ticker: str) -> pandas.DataFrame:   
        """

        Fetch stock price data from YFinance

        Args:
            ticker (str): Stock ticker

        Returns:
            pandas.DataFrame: Stock price data

        """
             
        ticker = yfinance.Ticker(ticker)
        hist = ticker.history(period='5y')

        if hist.empty:
            return pandas.DataFrame()

        return hist
    

class YFinanceCompanyFinancialsFetcher:
    """Using YFinance to fetch company financial data"""
    
    def fetch(self, ticker: str) -> dict:
        """
        Fetch company financial data from YFinance

        Args:
            ticker (str): Stock ticker

        Returns:
            dict: Company financial data
        """
        
        ticker_obj = yfinance.Ticker(ticker)
        info = ticker_obj.info
        balance_sheet = ticker_obj.balance_sheet
        cashflow = ticker_obj.cashflow

        if not info or balance_sheet.empty or cashflow.empty:
            return None

        return {
            'info': info,
            'balance_sheet': balance_sheet,
            'cashflow': cashflow
        }
