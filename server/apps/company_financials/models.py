from django.db import models

class CompanyFinancials(models.Model):
    ticker = models.CharField(max_length=10)
    fiscal_year = models.IntegerField()
    total_revenue = models.BigIntegerField(null=True, blank=True)
    normalized_ebitda = models.BigIntegerField(null=True, blank=True)
    stockholders_equity = models.BigIntegerField(null=True, blank=True)
    free_cash_flow = models.BigIntegerField(null=True, blank=True)
    capital_expenditures = models.BigIntegerField(null=True, blank=True)
    total_assets = models.BigIntegerField(null=True, blank=True)
    total_liabilities = models.BigIntegerField(null=True, blank=True)
    gross_profit = models.BigIntegerField(null=True, blank=True)
    net_income_loss = models.BigIntegerField(null=True, blank=True)
    operating_expenses = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CompanyFinancials for Company ID {self.ticker} for fiscal year {self.fiscal_year}"

    class Meta:
        verbose_name = "Company Financial"
        verbose_name_plural = "Company Financials"