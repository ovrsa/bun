from ..application.interfaces import CompanyProfileFetcher
from ..models import CompanyProfile
import requests
import yfinance
import pandas

class YFinanceCompanyProfileFetcher(CompanyProfileFetcher):
    """YFinanceを使って企業情報を取得する"""

    def fetch(self, ticker: str):
        """
        company_info.models.CompanyProfile

        Args:
            ticker (str): 銘柄コード

        Returns:
            Dict: 企業情報
        """
        
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        session.get('https://finance.yahoo.com', timeout=5)
        stock_data = yfinance.Ticker(ticker, session=session)

        try:
            info = stock_data.info
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

        if not info:
            print(f"No data returned for {ticker}")
            return None

        company_profile_data = {
            'company_name': info.get('longName', ''),
            'exchange': info.get('exchange', ''),
            'market_category': info.get('quoteType', ''),
            'industry': info.get('industry', ''),
            'sector': info.get('sector', ''),
            'address': f"{info.get('address1', '')}, {info.get('city', '')}, {info.get('state', '')} {info.get('zip', '')}, {info.get('country', '')}",
            'phone_number': info.get('phone', ''),
            'website': info.get('website', ''),
            'founding_year': (
                info.get('companyOfficers')[0].get('yearBorn')
                if info.get('companyOfficers') and len(info.get('companyOfficers')) > 0
                else None
            ),
            'employee_count': info.get('fullTimeEmployees', 0),
            'outstanding_shares': info.get('sharesOutstanding', 0),
            'market_capitalization': info.get('marketCap', 0.0),
            'average_trading_volume_10d': info.get('averageVolume10days', 0),
            'business_description': info.get('longBusinessSummary', ''),
        }

        return company_profile_data


class YFinanceStockPriceFetcher:
    """ YFinanceを使って株価データを取得する """

    def fetch(self, ticker):
        """
        company_info.models.StockPrice

        Args:
            ticker (str): 銘柄コード

        Returns:
            List[Dict]: 株価データ
        """
        
        ticker = yfinance.Ticker(ticker)
        hist = ticker.history(period='5y')

        
        if hist.empty:
            return None

        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        hist['MA200'] = hist['Close'].rolling(window=200).mean()
        hist['Volume'] = hist['Volume'].astype('Int64')

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
            close = row['Close'] if pandas.notnull(row['Close']) else None
            high = row['High'] if pandas.notnull(row['High']) else None
            low = row['Low'] if pandas.notnull(row['Low']) else None
            ma20 = row['MA20'] if pandas.notnull(row['MA20']) else None
            ma50 = row['MA50'] if pandas.notnull(row['MA50']) else None
            ma200 = row['MA200'] if pandas.notnull(row['MA200']) else None
            rsi = row['RSI'] if pandas.notnull(row['RSI']) else None
            volume = row['Volume'] if not pandas.isnull(row['Volume']) else None

            data.append({
                'date': row['Date'],
                'close': close,
                'high': high,
                'low': low,
                'moving_average_20': ma20,
                'moving_average_50': ma50,
                'moving_average_200': ma200,
                'rsi': rsi,
                'volume': volume,
            })

        return data
    

class YFinanceCompanyFinancialsFetcher:
    """YFinanceを使って企業の財務情報を取得する"""
    
    def fetch(self,ticker):
        """
        company_info.models.CompanyFinancials

        Args:
            ticker (str): 銘柄コード

        Returns:
            List[Dict]: 財務データ
        """
        
        ticker = yfinance.Ticker(ticker)
        info = ticker.info
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow

        # 日付インデックスを datetime 型に変換
        balance_sheet.columns = pandas.to_datetime(balance_sheet.columns, errors='coerce')
        cashflow.columns = pandas.to_datetime(cashflow.columns, errors='coerce')

        # TODO削除：デバッグ用に行名を表示
        # print(f"\n=== ティッカー {ticker} のバランスシート情報の行名 ===")
        # print(balance_sheet.index.tolist())
        # print(f"\n=== ティッカー {ticker} のキャッシュフロー情報の行名 ===")
        # print(cashflow.index.tolist())

        # 財務情報を格納するための辞書
        data = {}

        # 各年度の情報を取得
        for date in balance_sheet.columns:
            # TODO: ロジックを分離
            try:
                fiscal_year = date.year  # 日付の年度を取得

                # バランスシートから株主資本（Equity）を動的に検索して取得
                stockholders_equity = None
                possible_equity_names = [item for item in balance_sheet.index if 'equity' in item.lower()]
                if possible_equity_names:
                    stockholders_equity = balance_sheet.loc[possible_equity_names[0], date]

                # キャッシュフローから設備投資 (Capital Expenditures) を動的に検索して取得
                capital_expenditures = None
                possible_capex_names = [item for item in cashflow.index if 'capital' in item.lower() and 'expenditure' in item.lower()]
                if date in cashflow.columns and possible_capex_names:
                    capital_expenditures = cashflow.loc[possible_capex_names[0], date]

                # キャッシュフローからOperating Cash FlowおよびChange In Working Capitalを取得
                cash_from_operations = cashflow.loc['Operating Cash Flow', date] if 'Operating Cash Flow' in cashflow.index else None
                change_in_working_capital = cashflow.loc['Change In Working Capital', date] if 'Change In Working Capital' in cashflow.index else None

                # 財務情報を取得
                total_revenue = info.get("totalRevenue", None)
                ebitda = info.get("ebitda", None)
                net_income = info.get("netIncomeToCommon", None)
                free_cash_flow = info.get("freeCashflow", None)
                total_assets = balance_sheet.loc["Total Assets", date] if "Total Assets" in balance_sheet.index else None
                total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest", date] if "Total Liabilities Net Minority Interest" in balance_sheet.index else None

                # 財務比率の計算
                net_debt = info.get("totalDebt", None) - info.get("totalCash", None) if info.get("totalDebt", None) and info.get("totalCash", None) else None
                enterprise_value = info.get("enterpriseValue", None)
                ebitda_margin = (ebitda / total_revenue) if ebitda and total_revenue else None
                net_debt_to_ebitda = (net_debt / ebitda) if net_debt is not None and ebitda else None
                roa = (net_income / total_assets) if net_income and total_assets else None
                roe = (net_income / stockholders_equity) if net_income and stockholders_equity else None
                debt_to_equity = (info.get("totalDebt", None) / stockholders_equity) if info.get("totalDebt", None) and stockholders_equity else None
                operating_margin = (cash_from_operations / total_revenue) if cash_from_operations and total_revenue else None

                # 取得したデータを年度ごとに格納
                data[fiscal_year] = {
                    "fiscal_year": fiscal_year,
                    "total_revenue": total_revenue,
                    "normalized_ebitda": ebitda,
                    "stockholders_equity": stockholders_equity,
                    "free_cash_flow": free_cash_flow,
                    "capital_expenditures": capital_expenditures,
                    "total_assets": total_assets,
                    "total_liabilities": total_liabilities,
                    "gross_profit": info.get("grossMargins", None),
                    "net_income_loss": net_income,
                    "net_debt": net_debt,
                    "enterprise_value": enterprise_value,
                    "ebitda_margin": ebitda_margin,
                    "net_debt_to_ebitda": net_debt_to_ebitda,
                    "roa": roa,
                    "roe": roe,
                    "debt_to_equity": debt_to_equity,
                    "operating_margin": operating_margin,
                    "cash_from_operations": cash_from_operations,
                    "change_in_working_capital": change_in_working_capital
                }

            except KeyError as e:
                print(f"ティッカー {ticker}: 該当日付 {date} のデータが見つかりませんでした。キーエラー: {e}")
                continue
            except Exception as e:
                print(f"ティッカー {ticker}: データ取得中に予期しないエラーが発生しました。エラー: {e}")
                continue

        return data
