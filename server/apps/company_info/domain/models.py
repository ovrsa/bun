from django.db import models


class TickerReference(models.Model):
    ticker = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'company_info_ticker_reference'

    def __str__(self):
        return self.ticker


class CompanyProfile(models.Model):
    ticker = models.ForeignKey(TickerReference, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=50)
    market_category = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
    founding_year = models.IntegerField(null=True)
    employee_count = models.IntegerField(null=True)
    outstanding_shares = models.PositiveBigIntegerField(null=True)
    market_capitalization = models.FloatField(null=True)
    average_trading_volume_10d = models.BigIntegerField(null=True, blank=True)
    business_description = models.TextField(null=True,)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_info_company_profile'

    def __str__(self):
        return self.company_name


class StockPrice(models.Model):
    ticker = models.ForeignKey(
        TickerReference, on_delete=models.CASCADE, related_name='stock_prices')
    date = models.DateField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    moving_average_20 = models.FloatField(null=True, blank=True)
    moving_average_50 = models.FloatField(null=True, blank=True)
    moving_average_200 = models.FloatField(null=True, blank=True)
    rsi = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_info_stock_price'
        unique_together = ('ticker', 'date')
        ordering = ['date']

    def __str__(self):
        return self.ticker.company_name + ' ' + str(self.date)


class CompanyFinancials(models.Model):
    ticker = models.ForeignKey(TickerReference, on_delete=models.CASCADE, related_name='company_financials')
    fiscal_year = models.IntegerField()
    total_revenue = models.FloatField(null=True, blank=True)
    normalized_ebitda = models.FloatField(null=True, blank=True)
    stockholders_equity = models.FloatField(null=True, blank=True)
    free_cash_flow = models.FloatField(null=True, blank=True)
    capital_expenditures = models.FloatField(null=True, blank=True)
    total_assets = models.FloatField(null=True, blank=True)
    total_liabilities = models.FloatField(null=True, blank=True)
    gross_profit = models.FloatField(null=True, blank=True)
    net_income_loss = models.FloatField(null=True, blank=True)
    net_debt = models.FloatField(null=True, blank=True)
    enterprise_value = models.FloatField(null=True, blank=True)
    ebitda_margin = models.FloatField(null=True, blank=True)
    net_debt_to_ebitda = models.FloatField(null=True, blank=True)
    roa = models.FloatField(null=True, blank=True)
    roe = models.FloatField(null=True, blank=True)
    debt_to_equity = models.FloatField(null=True, blank=True)
    operating_margin = models.FloatField(null=True, blank=True)
    cash_from_operations = models.FloatField(null=True, blank=True)
    change_in_working_capital = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_info_company_financials'
        unique_together = ('ticker', 'fiscal_year')
        ordering = ['fiscal_year']

    def __str__(self):
        return self.ticker.ticker + ' ' + str(self.fiscal_year)
