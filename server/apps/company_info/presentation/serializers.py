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
        fields = '__all__'