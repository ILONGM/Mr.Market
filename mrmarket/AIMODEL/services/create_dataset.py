import pandas as pd
import numpy as np
from AIMODEL.models import MarketData

def create_dataset():
    """
    Récupère les données de la base et construit un dataset avec les variations et les indicateurs.
    """
    print("📥 Chargement des données depuis la base de données...")

    # Charge les données de la base
    data = pd.DataFrame(list(MarketData.objects.all().values()))

    if data.empty:
        print("⚠️ Aucune donnée disponible pour l'entraînement.")
        return None

    # Trier les données par date
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date").set_index("date")

    # Sélectionner les features utiles pour l'entraînement
    features = [
        "variation_sp500", "variation_nasdaq", "variation_dowjones",
        "variation_crude_oil", "variation_gold", "variation_eur_usd",
        "variation_treasury_10y", "variation_vix",
        "vix", "eur_usd", "treasury_10y"
    ]

    # Créer le dataset en gardant uniquement les features sélectionnées
    dataset = data[features]

    print("✅ Dataset créé avec succès !")
    print(dataset.head())
    return dataset
