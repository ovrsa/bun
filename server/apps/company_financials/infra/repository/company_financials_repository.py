from django.db import transaction

from company_financials.models import CompanyFinancials
from company_financials.core.repository.company_financials_repository import CompanyFinancialsRepository


class CompanyFinancialsRepository(CompanyFinancialsRepository):
    
    def save(self, data_list: list) -> None:
        with transaction.atomic():
            for data in data_list:
                existing_financials = CompanyFinancials.objects.filter(
                    ticker=data.get('symbol'),
                    fiscal_year=data.get('fiscal_year')
                ).first()
                if not existing_financials:
                    self._create(data)

    def _create(self, data: dict) -> None:
        if not data.get('symbol'):
            raise ValueError("Symbol cannot be null when creating a new financial record.")

        CompanyFinancials.objects.create(
            ticker=data.get('symbol'),
            fiscal_year=data.get('fiscal_year'),
            total_revenue=data.get('total_revenue'),
            normalized_ebitda=data.get('ebitda'),
            stockholders_equity=data.get('stockholders_equity'),
            free_cash_flow=data.get('free_cash_flow'),
            capital_expenditures=data.get('capital_expenditure'),
            total_assets=data.get('total_assets'),
            total_liabilities=data.get('total_liabilities'),
            gross_profit=data.get('gross_profit'),
            net_income_loss=data.get('net_income_loss'),
            operating_expenses=data.get('operating_expenses'),
        )

    def fetch(self, symbol: str, start_year: int = None, end_year: int = None) -> list:
        query = CompanyFinancials.objects.filter(ticker=symbol)
        if start_year:
            query = query.filter(fiscal_year__gte=start_year)
        if end_year:
            query = query.filter(fiscal_year__lte=end_year)
        return query.order_by('-fiscal_year')

