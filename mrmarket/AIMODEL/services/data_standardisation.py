from AIMODEL.models import MarketData

import pandas as pd

#Fonction permetant de normaliser les features (à reprendre demain)
def feature_normalize(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    return (dataset - mu) / sigma

