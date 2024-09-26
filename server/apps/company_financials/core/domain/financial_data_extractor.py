class FinancialDataExtractor:
    """財務データの抽出と変換を行うドメインサービス"""

    concept_mapping = {
        'fiscal_year': ['year'],
        'total_assets': ['us-gaap_Assets', 'ifrs_Assets'],
        'total_liabilities': ['us-gaap_Liabilities', 'ifrs_Liabilities'],
        'stockholders_equity': ['us-gaap_StockholdersEquity', 'us-gaap_Equity', 'ifrs_Equity'],
        'net_income': ['us-gaap_NetIncomeLoss', 'ifrs_ProfitLoss'],
        'capital_expenditure': [
            'us-gaap_PaymentsToAcquirePropertyPlantAndEquipment',
            'us-gaap_PaymentsToAcquireProductiveAssets'
        ],
        'gross_profit': ['us-gaap_GrossProfit'],
        'operating_expenses': ['us-gaap_OperatingExpenses'],
        'total_revenue': ['us-gaap_Revenues', 'ifrs_Revenue'],
        'ebitda': ['us-gaap_OperatingIncomeLoss', 'ifrs_OperatingProfit'],
        'normalized_ebitda': ['us-gaap_OperatingIncomeLoss', 'ifrs_OperatingProfit'],
        'net_income_loss': ['us-gaap_NetIncomeLoss', 'ifrs_ProfitLoss'],
        'free_cash_flow': ['us-gaap_NetCashProvidedByUsedInOperatingActivities'],
    }

    def extract_financial_info(self, data: dict) -> list:
        """データから財務情報を抽出
        
        Args:
            data (dict): APIから取得したデータ

        Returns:
            list: 財務情報のリスト
        """
        symbol = data.get('symbol')
        if not symbol:
            return []

        financial_info_list = []
        for entry in data.get('data', []):
            result = self._extract_single_entry(entry, symbol)
            if result:
                financial_info_list.append(result)
        return financial_info_list

    def _extract_single_entry(self, entry: dict, symbol: str) -> dict:
        """各エントリから財務データを抽出する。"""
        financial_data = entry.get('report', {})
        if not financial_data:
            return None

        bs_data = financial_data.get('bs', [])
        ic_data = financial_data.get('ic', [])
        cf_data = financial_data.get('cf', [])

        result = {'symbol': symbol}
        result['fiscal_year'] = entry.get('year', None)
        result['free_cash_flow'] = self._calculate_free_cash_flow(cf_data)
        result['ebitda'] = self._calculate_ebitda(ic_data, cf_data)

        for key, concepts in self.concept_mapping.items():
            if key not in result:  # 既に計算済みの項目を除外
                result[key] = self._find_value_in_reports(concepts, bs_data, ic_data, cf_data)

        return result

    def _calculate_free_cash_flow(self, cf_data: list) -> float:
        """フリーキャッシュフローを計算"""
        net_cash_operating = self._find_value_in_report(
            ['us-gaap_NetCashProvidedByUsedInOperatingActivities'], cf_data)
        capex = self._find_value_in_report(self.concept_mapping['capital_expenditure'], cf_data)
        if net_cash_operating is not None and capex is not None:
            return net_cash_operating - capex
        return None

    def _calculate_ebitda(self, ic_data: list, cf_data: list) -> float:
        """EBITDAを計算"""
        operating_income = self._find_value_in_report(self.concept_mapping['ebitda'], ic_data)
        depreciation_amortization = self._find_value_in_report(
            ['us-gaap_DepreciationDepletionAndAmortization'], cf_data)
        if operating_income is not None and depreciation_amortization is not None:
            return operating_income + depreciation_amortization
        return None

    def _find_value_in_reports(self, concepts, bs_data: list, ic_data: list, cf_data: list) -> float:
        """複数のレポートから値を検索"""
        return (
            self._find_value_in_report(concepts, bs_data) or
            self._find_value_in_report(concepts, ic_data) or
            self._find_value_in_report(concepts, cf_data)
        )

    @staticmethod
    def _find_value_in_report(concepts, report_data):
        """単一のレポートから値を検索"""
        if not isinstance(concepts, list):
            concepts = [concepts]
        for concept in concepts:
            for item in report_data:
                if item['concept'] == concept:
                    return item['value']
        return None

