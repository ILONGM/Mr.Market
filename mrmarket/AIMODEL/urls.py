from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage, name="homepage"),
    path("chart/", views.plot_market_data, name="chart"),
]
