from django.db import models

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10 , unique=True)
    exchange = models.CharField(max_length=50)
    market_category = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
    founding_year = models.IntegerField()
    employee_count = models.IntegerField()
    outstanding_shares = models.PositiveBigIntegerField(null=True, blank=True)
    market_capitalization = models.FloatField()
    average_trading_volume_10d = models.BigIntegerField(null=True, blank=True)
    business_description = models.TextField()

    class Meta:
        db_table = 'company_info_companyprofile'
        app_label = 'company_info'

    def __str__(self):
        return self.company_name
    
class BusinessSegment(models.Model):
    ticker = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='business_segments')
    segment_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.segment_name

class StockPrice(models.Model):
    ticker = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='stock_prices')
    date = models.DateField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    moving_average_20 = models.FloatField(null=True, blank=True)
    moving_average_50 = models.FloatField(null=True, blank=True)
    moving_average_200 = models.FloatField(null=True, blank=True)
    rsi = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'company_info_stockprice'
        unique_together = ('ticker', 'date')
        ordering = ['date']

    def __str__(self):
        return self.ticker.company_name + ' ' + str(self.date)

class CompanyFinancials(models.Model):
    ticker = models.ForeignKey(CompanyProfile,   on_delete=models.CASCADE)
    fiscal_year = models.IntegerField()
    total_revenue = models.FloatField()
    normalized_ebitda = models.FloatField()
    stockholders_equity = models.FloatField()
    free_cash_flow = models.FloatField()
    capital_expenditures = models.FloatField()
    total_assets = models.FloatField()
    total_liabilities = models.FloatField()
    gross_profit = models.FloatField()
    net_income_loss = models.FloatField()
    net_debt = models.FloatField()
    enterprise_value = models.FloatField()
    ebitda_margin = models.FloatField()
    net_debt_to_ebitda = models.FloatField()
    roa = models.FloatField()
    roe = models.FloatField()
    debt_to_equity = models.FloatField()
    operating_margin = models.FloatField()
    cash_from_operations = models.FloatField()
    change_in_working_capital = models.FloatField()

    def __str__(self):
        return self.ticker.company_name + ' ' + str(self.fiscal_year)
