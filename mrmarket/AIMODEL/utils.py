#test function to check utils.file is working
def test_function():
    return "Utils module is working!"

#imports required to create the fetch_function_data
import yfinance as yf
import time
from datetime import datetime, timedelta
from .models import MarketData


def fetch_market_data():
    """
    get data from Yahoofinance and store it in the database.
    """
    tickers = {
        "crude_oil": "CL=F",
        "eur_usd": "EURUSD=X",
        "gold": "GC=F",
        "dowjones": "^DJI",
        "sp500": "^GSPC",
        "nasdaq": "^IXIC",
        "treasury_10y": "^TNX",
        "vix": "^VIX"
    }



    # dowload of the historic prices for selected indicator
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 5)
    # selection of the "close" price for each selected indicator

    data = yf.download(list(tickers.values()), start=start_date, end=end_date, interval="1d")["Close"]


        #print(data.head())
   # print("*************")
    print(data.columns)

    # Renommer les colonnes avec les noms des indicateurs
    data.rename(columns=tickers, inplace=True)
   # print("*************")
    print(data.columns)

    # Supprimer les valeurs manquantes (NaN)
    data.dropna(inplace=True)

    # Ajouter chaque ligne dans la base de données Django
    for date, row in data.iterrows():
        MarketData.objects.get_or_create(
            date=date,
            sp500=row[tickers["sp500"]],
            nasdaq=row[tickers["nasdaq"]],
            dowjones=row[tickers["dowjones"]],
            crude_oil=row[tickers["crude_oil"]],
            gold=row[tickers["gold"]],
            eur_usd=row[tickers["eur_usd"]],
            treasury_10y=row[tickers["treasury_10y"]],
            vix=row[tickers["vix"]],
            is_abnormal=False
        )

    print("✅ market data successfully updated !")


def update_variations():
    """
    Met à jour les variations en % pour chaque ligne de la base.
    """
    all_data = MarketData.objects.order_by("date")
    previous = None

    for entry in all_data:
        if previous:
            entry.variation_sp500 = ((entry.sp500 - previous.sp500) / previous.sp500) * 100 if previous.sp500 else None
            entry.variation_nasdaq = ((entry.nasdaq - previous.nasdaq) / previous.nasdaq) * 100 if previous.nasdaq else None
            entry.variation_dowjones = ((entry.dowjones - previous.dowjones) / previous.dowjones) * 100 if previous.dowjones else None
            entry.variation_crude_oil = ((entry.crude_oil - previous.crude_oil) / previous.crude_oil) * 100 if previous.crude_oil else None
            entry.variation_gold = ((entry.gold - previous.gold) / previous.gold) * 100 if previous.gold else None
            entry.variation_eur_usd = ((entry.eur_usd - previous.eur_usd) / previous.eur_usd) * 100 if previous.eur_usd else None
            entry.variation_treasury_10y = ((entry.treasury_10y - previous.treasury_10y) / previous.treasury_10y) * 100 if previous.treasury_10y else None
            entry.variation_vix = ((entry.vix - previous.vix) / previous.vix) * 100 if previous.vix else None

            entry.save()

        previous = entry

    print("update successfull")