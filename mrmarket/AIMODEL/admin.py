from django.contrib import admin
from .models import MarketData

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    #list_display = ('date', 'sp500', 'nasdaq', 'dowjones', 'crude_oil', 'gold', 'eur_usd', 'treasury_10y', 'vix', 'is_abnormal')
    list_display = (
        'date',
        'sp500', 'variation_sp500',
        'nasdaq', 'variation_nasdaq',
        'dowjones', 'variation_dowjones',
        'crude_oil', 'variation_crude_oil',
        'gold', 'variation_gold',
        'eur_usd', 'variation_eur_usd',
        'treasury_10y', 'variation_treasury_10y',
        'vix', 'variation_vix',
        'is_abnormal'
    )
    list_filter = ('is_abnormal',)
    search_fields = ('date',)

# Register your models here.
