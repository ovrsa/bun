from django.contrib import admin
from .models import CompanyProfile, BusinessSegment, StockPrice, StockVolume, CompanyFinancials

admin.site.register(CompanyProfile)
admin.site.register(BusinessSegment)
admin.site.register(StockPrice)
admin.site.register(StockVolume)
admin.site.register(CompanyFinancials)