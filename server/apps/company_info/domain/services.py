import pandas
import numpy

import logging

logger = logging.getLogger(__name__)

class CompanyProfileProcessor:
    """Company Profile data editing and processing"""

    @staticmethod
    def process_raw_data(raw_data: dict) -> dict:
        if not raw_data:
            logger.warning("No company profile data found")
            return {}

        company_profile_data = {
            'company_name': raw_data.get('longName', ''),
            'exchange': raw_data.get('exchange', ''),
            'market_category': raw_data.get('quoteType', ''),
            'industry': raw_data.get('industry', ''),
            'sector': raw_data.get('sector', ''),
            'address': f"{raw_data.get('address1', '')}, {raw_data.get('city', '')}, {raw_data.get('state', '')} {raw_data.get('zip', '')}, {raw_data.get('country', '')}",
            'phone_number': raw_data.get('phone', ''),
            'website': raw_data.get('website', ''),
            'founding_year': (
                raw_data.get('companyOfficers')[0].get('yearBorn')
                if raw_data.get('companyOfficers') and len(raw_data.get('companyOfficers')) > 0
                else None
            ),
            'employee_count': raw_data.get('fullTimeEmployees', 0),
            'outstanding_shares': raw_data.get('sharesOutstanding', 0),
            'market_capitalization': raw_data.get('marketCap', 0.0),
            'average_trading_volume_10d': raw_data.get('averageVolume10days', 0),
            'business_description': raw_data.get('longBusinessSummary', ''),
        }
        return company_profile_data


class StockPriceProcessor:
    """Stock price data editing and processing"""

    @staticmethod
    def process_raw_data(raw_data):
        if raw_data.empty:
            logger.warning("Received empty stock price data")
            return []

        try:
            # 移動平均の計算
            raw_data['MA20'] = raw_data['Close'].rolling(window=20).mean()
            raw_data['MA50'] = raw_data['Close'].rolling(window=50).mean()
            raw_data['MA200'] = raw_data['Close'].rolling(window=200).mean()

            raw_data['Volume'] = raw_data['Volume'].astype('Int64')

            # RSIの計算
            delta = raw_data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            raw_data['RSI'] = 100 - (100 / (1 + rs))

            raw_data.replace([pandas.NA, pandas.NaT, numpy.nan, numpy.inf, -numpy.inf], None, inplace=True)

            raw_data.reset_index(inplace=True)
            raw_data['Date'] = raw_data['Date'].dt.date

            processed_data = []
            for _, row in raw_data.iterrows():
                processed_data.append({
                    'date': row['Date'],
                    'close': row['Close'],
                    'high': row['High'],
                    'low': row['Low'],
                    'moving_average_20': row['MA20'],
                    'moving_average_50': row['MA50'],
                    'moving_average_200': row['MA200'],
                    'rsi': row['RSI'],
                    'volume': row['Volume'],
                })

            logger.info("Processed stock price data successfully")
            return processed_data

        except Exception as e:
            logger.error("Error processing stock price data: %s", e)
            raise


class FinancialDataProcessor:
    """Financial data editing and processing"""

    @staticmethod
    def process_financial_data(balance_sheet, cashflow, income_stmt):
        # 日付インデックスを datetime 型に変換
        balance_sheet.columns = pandas.to_datetime(balance_sheet.columns, errors='coerce')
        cashflow.columns = pandas.to_datetime(cashflow.columns, errors='coerce')
        income_stmt.columns = pandas.to_datetime(income_stmt.columns, errors='coerce')

        # インデックス名を小文字化して統一
        balance_sheet.index = balance_sheet.index.str.lower()
        cashflow.index = cashflow.index.str.lower()
        income_stmt.index = income_stmt.index.str.lower()

        data = {}
        # 共通の日付リストを作成
        dates = balance_sheet.columns.intersection(cashflow.columns).intersection(income_stmt.columns)

        # データ取得関数の定義
        def get_financial_item(dataframe, possible_names, date):
            for name in possible_names:
                if name in dataframe.index:
                    return dataframe.loc[name, date]
            return None

        for date in dates:
            try:
                fiscal_year = date.year

                # 株主資本を取得
                possible_equity_names = [
                    'stockholders equity', 'total stockholder equity',
                    'total shareholders equity', 'total equity',
                    'common stock equity', 'total equity gross minority interest'
                ]
                stockholders_equity = get_financial_item(balance_sheet, possible_equity_names, date)

                # 総負債を取得
                possible_liabilities_names = [
                    'total liabilities', 'total liab',
                    'total liabilities net minority interest'
                ]
                total_liabilities = get_financial_item(balance_sheet, possible_liabilities_names, date)

                # total_revenueを先に取得
                possible_total_revenue_names = ['total revenue']
                total_revenue = get_financial_item(income_stmt, possible_total_revenue_names, date)

                # 営業利益を取得し、営業利益率を計算
                possible_operating_income_names = [
                    'operating income', 'operating profit'
                ]
                operating_income = get_financial_item(income_stmt, possible_operating_income_names, date)
                operating_margin = (operating_income / total_revenue) if operating_income and total_revenue else None

                # 営業キャッシュフローを取得
                possible_cash_from_ops_names = [
                    'operating cash flow', 'total cash from operating activities',
                    'net cash provided by operating activities',
                    'cash flow from continuing operating activities'
                ]
                cash_from_operations = get_financial_item(cashflow, possible_cash_from_ops_names, date)

                # その他のデータを取得
                possible_capex_names = ['capital expenditures', 'capital expenditure']
                capital_expenditures = get_financial_item(cashflow, possible_capex_names, date)

                possible_change_in_wc_names = [
                    'change in working capital', 'change to net working capital',
                    'change in net working capital'
                ]
                change_in_working_capital = get_financial_item(cashflow, possible_change_in_wc_names, date)

                possible_net_income_names = ['net income', 'net income applicable to common shares']
                net_income = get_financial_item(income_stmt, possible_net_income_names, date)

                possible_ebitda_names = ['ebitda', 'normalized ebitda']
                ebitda = get_financial_item(income_stmt, possible_ebitda_names, date)

                possible_gross_profit_names = ['gross profit']
                gross_profit = get_financial_item(income_stmt, possible_gross_profit_names, date)

                # バランスシートから総資産を取得
                total_assets = get_financial_item(balance_sheet, ['total assets'], date)

                # ネットデットの計算
                possible_total_cash_names = ['cash', 'cash and cash equivalents', 'cash financial']
                total_cash = get_financial_item(balance_sheet, possible_total_cash_names, date) or 0
                possible_short_term_debt_names = ['short long term debt', 'short term debt', 'current debt']
                short_term_debt = get_financial_item(balance_sheet, possible_short_term_debt_names, date) or 0
                possible_long_term_debt_names = ['long term debt']
                long_term_debt = get_financial_item(balance_sheet, possible_long_term_debt_names, date) or 0
                net_debt = (short_term_debt + long_term_debt) - total_cash

                # 財務比率の計算
                ebitda_margin = (ebitda / total_revenue) if ebitda and total_revenue else None
                net_debt_to_ebitda = (net_debt / ebitda) if ebitda and ebitda != 0 else None
                roa = (net_income / total_assets) if net_income and total_assets else None
                roe = (net_income / stockholders_equity) if net_income and stockholders_equity else None
                debt_to_equity = (total_liabilities / stockholders_equity) if total_liabilities and stockholders_equity else None

                # フリーキャッシュフローの取得
                possible_free_cash_flow_names = ['free cash flow']
                free_cash_flow = get_financial_item(cashflow, possible_free_cash_flow_names, date)

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
                    "gross_profit": gross_profit,
                    "net_income_loss": net_income,
                    "net_debt": net_debt,
                    "enterprise_value": None,  # 必要に応じて計算
                    "ebitda_margin": ebitda_margin,
                    "net_debt_to_ebitda": net_debt_to_ebitda,
                    "roa": roa,
                    "roe": roe,
                    "debt_to_equity": debt_to_equity,
                    "operating_margin": operating_margin,
                    "cash_from_operations": cash_from_operations,
                    "change_in_working_capital": change_in_working_capital,
                }

            except Exception as e:
                logger.error(f'Error processing financial data for {date}: {e}')
                continue

        return data
