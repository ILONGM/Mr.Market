from django.db import models

# Create your models here.

class MarketData(models.Model):
    date = models.DateField(unique=True)
    sp500 = models.FloatField()
    nasdaq = models.FloatField()
    dowjones = models.FloatField()
    crude_oil = models.FloatField()
    gold = models.FloatField()
    eur_usd = models.FloatField()
    treasury_10y = models.FloatField()
    vix = models.FloatField()
    is_abnormal = models.BooleanField()

    variation_sp500 = models.FloatField(null=True, blank=True)
    variation_nasdaq = models.FloatField(null=True, blank=True)
    variation_dowjones = models.FloatField(null=True, blank=True)
    variation_crude_oil = models.FloatField(null=True, blank=True)
    variation_gold = models.FloatField(null=True, blank=True)
    variation_eur_usd = models.FloatField(null=True, blank=True)
    variation_treasury_10y = models.FloatField(null=True, blank=True)
    variation_vix = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {'Abnormal' if self.is_abnormal else 'Normal'}"
