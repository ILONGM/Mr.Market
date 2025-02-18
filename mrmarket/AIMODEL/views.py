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

# Create your views here.
