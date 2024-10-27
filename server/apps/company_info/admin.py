from django.contrib import admin
from .models import CompanyProfile, StockPrice, CompanyFinancials

admin.site.register(CompanyProfile)
admin.site.register(StockPrice)
admin.site.register(CompanyFinancials)