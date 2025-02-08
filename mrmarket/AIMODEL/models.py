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

    def __str__(self):
        return f"{self.date} - {'Abnormal' if self.is_abnormal else 'Normal'}"
