from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import pprint
# ------------------------
# URL de la page de RESULTATS (liste d'annonces)
# ------------------------
## récuperer le lien d'accéder au page selon la trie par groupe des quatiers 
# exemple pour accéder au page des logements à Rennes Centre Ville (qui appartient aux Quatiers Centre) dont le lien est :"https://www.ouestfrance-immo.com/louer/appartement/?lieux=100005"
# "Rennes Centre Ville": "100005" # le lien est commence par "https://www.ouestfrance-immo.com/louer/appartement/?lieux=" + paramètre( ici parametre est "100005")
link_trier_par_localisation ="https://www.ouestfrance-immo.com/louer/appartement/?colocation=0&lieux="
code_lieux =quartiers = {
    "Quartiers Centre": {
        "Rennes Centre Ville": "100005",
        "Rennes Thabor": "100023",
        "Rennes Saint-Helier": "100019"
    },

    "Quartiers Ouest": {
        "Rennes Arsenal - Redon": "100000",
        "Rennes Cleunay": "100006",
        "Rennes Bourg L'evêque": "100003"
    },

    "Quartiers Nord-Est": {
        "Rennes Maurepas": "100014",
        "Rennes Beaulieu": "100001",
        "Rennes Jeanne D'arc": "100010",
        "Rennes Longs Champs": "100012"
    },

    "Quartiers Nord-Ouest": {
        "Rennes Beauregard": "100002",
        "Rennes Villejean": "100024",
        "Rennes Nord Saint-Martin": "100015"
    }
}
dict_quartier_et_liens_trouvé ={}
for quartiers , val in code_lieux.items():
    
    liste_lien =[]
    for quart , param in val.items() :
        liste_lien.append(link_trier_par_localisation+param)
    dict_quartier_et_liens_trouvé[quartiers] = liste_lien









