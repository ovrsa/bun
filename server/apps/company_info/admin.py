from django.contrib import admin
from .models import CompanyProfile, BusinessSegment, StockPrice, CompanyFinancials

admin.site.register(CompanyProfile)
admin.site.register(BusinessSegment)
admin.site.register(StockPrice)
admin.site.register(CompanyFinancials)