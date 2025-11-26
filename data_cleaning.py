import pandas as pd
import numpy as np

annonces = pd.read_csv("annonces.csv" , delimiter="," , decimal=".") 

#Sélectionner les colonnes d'intérêt
annonces = annonces.loc[ :  ,['Loyer' , "Surface habitable" ,'Dont charges' , 'Pièces' ,'label_eco' , 'kWh/m² .an' ,'kgCO2/m² .an' , 'Quartiers'  ]]
annonces.rename(columns={'Loyer' :  "Loyer_TTC" ,
                         "Surface habitable" :"Surface",
                        'Dont charges': 'Charges' ,
                        'kWh/m² .an' :"kWh" 
                         ,'kgCO2/m² .an' :"kgCO2" }, inplace=True)
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

# Estimer les valeurs des charges manquantes en fonction de Loyer TTC
min_loyer = annonces['Loyer_TTC'].min()
max_loyer = annonces['Loyer_TTC'].max()
seuils_loyer = np.linspace(min_loyer, max_loyer, 6)
annonces['Loyer_Groupe'] = pd.cut(annonces['Loyer_TTC'], bins=seuils_loyer, include_lowest=True)

print(annonces["Loyer_Groupe"].value_counts(dropna=True))

annonces["Charges"] = annonces.groupby('Loyer_Groupe')['Charges'].transform(lambda x : x.fillna(round(x.mean(), 2)))
print(annonces[annonces.isna().any(axis=1)]) 

#Exporter les données nettoyées
df_to_export = annonces.drop(columns=['Loyer_Groupe'])
df_to_export.to_csv("Loyer_Rennes.csv", sep=";" , decimal="." , index=False)
print("Données nettoyées exportées vers 'Loyer_Rennes.csv'")