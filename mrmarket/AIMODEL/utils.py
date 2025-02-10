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
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "Crude Oil": "CL=F",
        "Gold": "GC=F",
        "EUR/USD": "EURUSD=X",
        "US 10Y Treasury": "^TNX",
        "VIX": "^VIX"
    }

    # Définir la période de récupération des données
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 5)  # 5 ans d'historique

    # Télécharger les données de Yahoo Finance
    data = yf.download(list(tickers.values()), start=start_date, end=end_date, interval="1d")
    data = data["Close"]
    print(data)
    # Renommer les colonnes avec les noms des indicateurs
    data.columns = tickers.keys()

    # Supprimer les valeurs manquantes (NaN)
    data.dropna(inplace=True)

    print("Colonnes récupérées :", data.columns)
    print("Colonnes attendues :", list(tickers.keys()))

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
            is_abnormal=False  # Valeur par défaut, l'IA mettra à jour plus tard
        )

    print("✅ Données du marché mises à jour avec succès !")
