from rest_framework import serializers
from ..models import CompanyProfile
from ..models import BusinessSegment
from ..models import CompanyFinancials
from ..models import StockPrice

class CompanyProfileSerializer(serializers.ModelSerializer):
    business_segments = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name',
            'market_category',
            'industry',
            'sector',
            'address',
            'phone_number',
            'website',
            'founding_year',
            'employee_count',
            'outstanding_shares',
            'market_capitalization',
            'average_trading_volume_10d',
            'business_segments',
            'business_description',
        ]

class BusinessSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSegment
        fields = ['segment_name', 'description']


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = [
            'date',
            'close',
            'high',
            'low',
            'moving_average_20',
            'moving_average_50',
            'moving_average_200',
            'rsi',
            'volume',
        ]


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
            'net_debt',
            'enterprise_value',
            'ebitda_margin',
            'net_debt_to_ebitda',
            'roa',
            'roe',
            'debt_to_equity',
            'operating_margin',
            'cash_from_operations',
            'change_in_working_capital',
        ]
