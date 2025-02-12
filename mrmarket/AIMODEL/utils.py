#test function to check utils.file is working
def test_function():
    return "Utils module is working!"

#imports required to create the fetch_function_data
import yfinance as yf
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
