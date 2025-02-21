import numpy as np

#Fonction permetant de normaliser les features (à reprendre demain)
def feature_normalize(dataset):
    """
       Normalise le dataset : (X - mu) / sigma
    """
    print("Normalisation des données...")

    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    normalized_dataset = (dataset - mu) / sigma
    print("✅ Normalisation terminée !")
    return normalized_dataset