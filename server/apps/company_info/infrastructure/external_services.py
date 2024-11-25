from ..application.interfaces import CompanyProfileFetcher
import requests
import yfinance
import pandas


class YFinanceCompanyProfileFetcher(CompanyProfileFetcher):

    def fetch(self, ticker: str) -> dict:

        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        session.get('https://finance.yahoo.com', timeout=5)
        stock_data = yfinance.Ticker(ticker, session=session)

        info = stock_data.info

        if not info:
            return None

        return info


class YFinanceStockPriceFetcher:

    def fetch(self, ticker: str) -> pandas.DataFrame:

        ticker = yfinance.Ticker(ticker)
        hist = ticker.history(period='5y')

        if hist.empty:
            return pandas.DataFrame()

        return hist


class YFinanceCompanyFinancialsFetcher:

    def fetch(self, ticker: str) -> dict:

        ticker_obj = yfinance.Ticker(ticker)
        balance_sheet = ticker_obj.balance_sheet
        cashflow = ticker_obj.cashflow
        income_stmt = ticker_obj.financials

        if balance_sheet.empty or cashflow.empty or income_stmt.empty:
            return None

        return {
            'balance_sheet': balance_sheet,
            'cashflow': cashflow,
            'income_stmt': income_stmt
        }
