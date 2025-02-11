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
    column_map = {
        "CL=F": "Crude Oil",
        "EURUSD=X": "EUR/USD",
        "GC=F": "Gold",
        "^DJI": "Dow Jones",
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^TNX": "US 10Y Treasury",
        "^VIX": "VIX"
    }



    # dowload of the historic prices for selected indicator
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 5)
    # selection of the "close" price for each selected indicator
    data = yf.download(list(column_map.values()), start=start_date, end=end_date, interval="1d")["Close"]

    #print(data.head())
   # print("*************")
    #print(data.columns)

    # Renommer les colonnes avec les noms des indicateurs
    data.rename(columns=column_map, inplace=True)
   # print("*************")
   # print(data.columns)

    # Supprimer les valeurs manquantes (NaN)
    data.dropna(inplace=True)


    # Ajouter chaque ligne dans la base de données Django
    for date, row in data.iterrows():
        MarketData.objects.get_or_create(
            date=date,
            sp500=row["S&P 500"],
            nasdaq=row["NASDAQ"],
            dowjones=row["Dow Jones"],
            crude_oil=row["Crude Oil"],
            gold=row["Gold"],
            eur_usd=row["EUR/USD"],
            treasury_10y=row["US 10Y Treasury"],
            vix=row["VIX"],
            is_abnormal=False
        )

    print("✅ market data successfully updated !")
