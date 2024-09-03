from django.db import models


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    country = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    exchange = models.CharField(max_length=255)
    ipo_date = models.DateField(null=True, blank=True)
    market_capitalization = models.BigIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    share_outstanding = models.DecimalField(
        max_digits=15, decimal_places=8, null=True, blank=True)
    website_url = models.URLField(max_length=255, null=True, blank=True)
    logo_url = models.URLField(max_length=255, null=True, blank=True)
    finnhub_industry = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
