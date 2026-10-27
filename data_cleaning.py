import pandas as pd
import numpy as np

annonces = pd.read_csv("data_raw/annonces.csv" , delimiter="," , decimal=".") 
annonces = annonces.drop_duplicates()

#Sélectionner les colonnes d'intérêt
annonces = annonces.loc[ :  ,['Loyer' , "Surface habitable" ,'Dont charges' , 'Pièces' ,'label_eco' , 'kWh/m² .an' ,'kgCO2/m² .an' , 'Quartiers' , 'Type stationnement' ]]
annonces.rename(columns={'Loyer' :  "Loyer_TTC" ,
                         "Surface habitable" :"Surface",
                        'Dont charges': 'Charges' ,
                        'kWh/m² .an' :"kWh" 
                         ,'kgCO2/m² .an' :"kgCO2" , "Type stationnement" : "station" }, inplace=True)
annonces = annonces[~annonces["Loyer_TTC"].isna()]
#identifier les lignes avec des valeurs manquantes
print(annonces[annonces.isna().any(axis=1)]) 

#Remplacer les valeurs manquantes dans la colonne "Pièces" par 1
annonces.loc[ annonces["Pièces"].isnull() , "Pièces"] = 1 
print(annonces[annonces.isna().any(axis=1)]) 

#visualiser les effectifs par catégorie dans la colonne "label_eco"
effectifs = annonces.groupby('label_eco').size()
print(effectifs)
#Supprimer les lignes dont la valeur dans colonne "label_eco" est NC (Non Classé)
annonces = annonces[annonces["label_eco"] != "NC"]

#regrouper les catégories NS (Non Significative) dans la catégorie A
annonces.loc[(annonces["label_eco"]=="NS") |  (annonces["label_eco"]=="A") | (annonces["label_eco"]=="B")  , "label_eco"] = "B+"
print(annonces[annonces.isna().any(axis=1)]) 

#Remplacer les valeurs manquantes dans la colonne "kWh/m² .an" par la moyenne de la colonne selon le groupe "label_eco"
print(annonces.groupby('label_eco')['kWh'].mean())
annonces['kWh'] = annonces.groupby('label_eco')['kWh'].transform(lambda x: x.fillna(x.mean()))
annonces['kgCO2'] = annonces.groupby('label_eco')['kgCO2'].transform(lambda x: x.fillna(x.mean()))
print(annonces[annonces.isna().any(axis=1)]) 

# Estimer les valeurs des charges manquantes en fonction de surface
# Estimer les valeurs des charges manquantes en fonction de la surface (5 tranches de même effectif)
tranche_surface = pd.qcut(annonces["Surface"], 5)
annonces['Charges'] = annonces.groupby(tranche_surface, observed=True)['Charges'].transform(lambda x: x.fillna(x.mean()))

print(annonces[annonces.isna().any(axis=1)]) 

#retirer le coloc

prix_m2 = annonces["Loyer_TTC"] / annonces["Surface"]
surf_piece = annonces["Surface"] / annonces["Pièces"]

colocation = (prix_m2 < 8) | (surf_piece < 8)
print(colocation.sum(), "annonces retirées (colocations probables)")
annonces = annonces[~colocation]
#station -> reiseigner ou non
annonces["station"] = np.where(annonces["station"].isna() , "Non/Non_renseigner" ,annonces["station"] )

#Regrouper les types de stationnement en 4 catégories
annonces["station"] = annonces["station"].replace({
    "Non/Non_renseigner": "Aucun",
    "Garage fermé": "Garage", "Garage, Garage fermé": "Garage",
    "Garage, Sous-sol": "Garage", "Garage, Parking": "Garage",
    "Sous-sol": "Couvert/Sous-sol", "Stationnement en sous-sol": "Couvert/Sous-sol",
    "Couvert": "Couvert/Sous-sol", "Stationnement couvert": "Couvert/Sous-sol",
    "Parking": "Extérieur", "Aérien": "Extérieur", "Stationnement aérien": "Extérieur",
})
inconnues = set(annonces["station"]) - {"Aucun", "Garage", "Couvert/Sous-sol", "Extérieur"}
assert not inconnues, f"Stationnement non regroupé : {inconnues}"

#Exporter les données nettoyées
print(annonces.head())

annonces.to_csv("data_cleaning/annonces.csv", sep=";" , decimal="." , index=False)
print("Données nettoyées exportées vers 'data_cleaning/annonces.csv'")