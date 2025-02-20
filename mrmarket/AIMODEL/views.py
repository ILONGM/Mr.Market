from django.shortcuts import render
from .models import MarketData

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib
import pandas as pd
import base64


def homepage(request):
    return render(request, "homepage.html")

def plot_market_data(request):

    available_variables = ["sp500", "nasdaq", "dowjones", "crude_oil", "gold", "eur_usd", "treasury_10y", "vix"]
    selected_variable = request.GET.get("variable", "sp500")

    data = pd.DataFrame(list(MarketData.objects.all().values("date", selected_variable)))
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")

    # Générer le graphique avec Matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data[selected_variable], marker='', linestyle='-', label=selected_variable.upper())
    plt.xlabel("Date")
    plt.ylabel(selected_variable.upper())
    plt.title(f"Évolution de {selected_variable.upper()}")
    plt.legend()
    plt.grid(True)

    # Convertir le graphique en image pour Django
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    #string = urllib.parse.quote(buf.read())
    buf.close()

    # Rendre la page HTML avec le graphique
    return render(request, "market_chart.html", {
        "chart": image_base64,
        "available_variables": available_variables,
        "selected_variable": selected_variable.upper()
    })


import numpy as np
import seaborn as sns
from scipy.stats import norm


def plot_probability_distribution(request):
    """
    Affiche la distribution des variations en % sous forme d'une loi de probabilité.
    """
    available_variables = [
        "variation_sp500", "variation_nasdaq", "variation_dowjones",
        "variation_crude_oil", "variation_gold", "variation_eur_usd",
        "variation_treasury_10y", "variation_vix"
    ]

    selected_variable = request.GET.get("variable", "variation_sp500")

    # Récupérer les variations en % depuis la base de données
    data = pd.DataFrame(list(MarketData.objects.all().values(selected_variable)))

    # Vérifier si des données sont disponibles
    if data.empty:
        return render(request, "probability_chart.html", {
            "chart": None,
            "available_variables": available_variables,
            "selected_variable": selected_variable.upper(),
            "error": "⚠️ Aucune donnée disponible pour cette variable."
        })

    # Supprimer les valeurs NaN (données manquantes)
    data = data.dropna()

    # Extraire la colonne de variation
    variation_values = data[selected_variable]

    # Créer un histogramme normalisé et une courbe de densité (PDF)
    plt.figure(figsize=(10, 5))
    sns.histplot(variation_values, kde=True, stat="density", bins=30, color="blue", alpha=0.6)

    # Superposer une courbe de distribution normale ajustée
    mean, std = np.mean(variation_values), np.std(variation_values)
    x = np.linspace(min(variation_values), max(variation_values), 100)
    plt.plot(x, norm.pdf(x, mean, std), color="red", label="Courbe de distribution normale")

    plt.xlabel("Variation (%)")
    plt.ylabel("Densité de probabilité")
    plt.title(f"Distribution des variations de {selected_variable.upper()}")
    plt.legend()
    plt.grid(True)

    # Convertir le graphique en image pour Django
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Rendre la page HTML avec le graphique
    return render(request, "probability_chart.html", {
        "chart": image_base64,
        "available_variables": available_variables,
        "selected_variable": selected_variable.upper()
    })

# Create your views here.
