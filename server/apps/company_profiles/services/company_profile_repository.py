from datetime import datetime
from django.db import transaction
from django.utils.timezone import now
from ..models import CompanyProfile


class CompanyProfileRepository:
    """Repository class for CompanyProfile model"""

    @staticmethod
    def get_today_date_range():
        current_time = now()
        today_start = datetime.combine(
            current_time.date(), datetime.min.time())
        today_end = datetime.combine(current_time.date(), datetime.max.time())
        return today_start, today_end

    def get_cached_profile(self, symbol: str) -> CompanyProfile:
        today_start, today_end = self.get_today_date_range()
        return CompanyProfile.objects.filter(
            ticker=symbol,
            created_at__range=(today_start, today_end)
        ).first()

    def save_company_profile(self, data: dict) -> CompanyProfile:
        with transaction.atomic():
            existing_profile = self.get_cached_profile(data.get('ticker'))
            if existing_profile:
                return existing_profile

            return self.create_new_profile(data)

    def create_new_profile(self, data: dict) -> CompanyProfile:
        return CompanyProfile.objects.create(
            ticker=data.get('ticker'),
            company_name=data.get('name'),
            country=data.get('country'),
            currency=data.get('currency'),
            exchange=data.get('exchange'),
            ipo_date=data.get('ipo'),
            market_capitalization=data.get('marketCapitalization'),
            phone=data.get('phone'),
            share_outstanding=data.get('shareOutstanding'),
            website_url=data.get('weburl'),
            logo_url=data.get('logo'),
            finnhub_industry=data.get('finnhubIndustry'),
            created_at=now(),
        )
