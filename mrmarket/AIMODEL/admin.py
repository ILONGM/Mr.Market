from django.contrib import admin
from .models import MarketData

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'sp500', 'nasdaq', 'dowjones', 'crude_oil', 'gold', 'eur_usd', 'treasury_10y', 'vix', 'is_abnormal')
    list_filter = ('is_abnormal',)
    search_fields = ('date',)

# Register your models here.
