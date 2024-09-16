from rest_framework import serializers
from company_financials.models import CompanyFinancials

class CompanyFinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFinancials
        fields = [
            'fiscal_year',
            'total_revenue',
            'normalized_ebitda',
            'stockholders_equity',
            'free_cash_flow',
            'capital_expenditures',
            'total_assets',
            'total_liabilities',
            'gross_profit',
            'net_income_loss',
            'operating_expenses',
            'created_at'
        ]
