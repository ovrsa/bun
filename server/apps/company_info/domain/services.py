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
    def process_financial_data(info, balance_sheet, cashflow):

        data = {}
        for date in balance_sheet.columns:
            try:
                fiscal_year = date.year

                stockholders_equity = FinancialDataProcessor._get_value_from_index(
                    balance_sheet, date, 'equity'
                )
                capital_expenditures = FinancialDataProcessor._get_value_from_index(
                    cashflow, date, 'capital', 'expenditure'
                )
                cash_from_operations = cashflow.loc['Operating Cash Flow', date] if 'Operating Cash Flow' in cashflow.index and date in cashflow.columns else None
                change_in_working_capital = cashflow.loc['Change In Working Capital', date] if 'Change In Working Capital' in cashflow.index and date in cashflow.columns else None
                total_assets = balance_sheet.loc['Total Assets', date] if 'Total Assets' in balance_sheet.index and date in balance_sheet.columns else None
                total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest', date] if 'Total Liabilities Net Minority Interest' in balance_sheet.index and date in balance_sheet.columns else None

                # 財務指標の計算
                total_revenue = info.get("totalRevenue", None)
                ebitda = info.get("ebitda", None)
                net_income = info.get("netIncomeToCommon", None)
                free_cash_flow = info.get("freeCashflow", None)
                net_debt = (info.get("totalDebt", 0) - info.get("totalCash", 0)) if info.get("totalDebt") else None
                enterprise_value = info.get("enterpriseValue", None)
                ebitda_margin = (ebitda / total_revenue) if ebitda and total_revenue else None
                net_debt_to_ebitda = (net_debt / ebitda) if net_debt is not None and ebitda else None
                roa = (net_income / total_assets) if net_income and total_assets else None
                roe = (net_income / stockholders_equity) if net_income and stockholders_equity else None
                debt_to_equity = (info.get("totalDebt", None) / stockholders_equity) if info.get("totalDebt", None) and stockholders_equity else None
                operating_margin = (cash_from_operations / total_revenue) if cash_from_operations and total_revenue else None

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
                    "change_in_working_capital": change_in_working_capital,
                }

            except Exception as e:
                logger.error(f'Error processing financial data for {date}: {e}')
                continue

        return data


    @staticmethod
    def _get_value_from_index(df, date, *keywords):
        """Get value from DataFrame by index"""
        for item in df.index:
            if all(keyword.lower() in item.lower() for keyword in keywords):
                return df.loc[item, date]
        return None
