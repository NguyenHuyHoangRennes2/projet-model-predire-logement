from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pandas as pd
from chemin_vers_liste_annonces import dict_quartier_et_liens_trouvé
# ------------------------
# URL de la page de RESULTATS (liste d'annonces)
# ------------------------
## récuperer le lien d'accéder au page selon la trie par groupe des quatiers 
# exemple pour accéder au page des logements à Rennes Centre Ville (qui appartient aux Quatiers Centre) dont le lien est :"https://www.ouestfrance-immo.com/louer/appartement/?lieux=100005"
# "Rennes Centre Ville": "100005" # le lien est commence par "https://www.ouestfrance-immo.com/louer/appartement/?lieux=" + paramètre( ici parametre est "100005")
dict_quartier_et_liens_trouvé =dict_quartier_et_liens_trouvé
# Dictionnaire pour stocker les liens par quartier
données =[]
for quartiers , liens in dict_quartier_et_liens_trouvé.items():
    for lien in liens :
        URL = lien
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(URL)

        wait = WebDriverWait(driver, 20)

        # ---------------------------------------
        # 1) Fermer popup cookies "Accepter et fermer"
        # ---------------------------------------
        try:
            bouton_cookie = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Accepter et fermer')]")
                )
            )
            bouton_cookie.click()
            print("Popup cookies fermé.")
        except TimeoutException:
            print("Popup cookies non trouvé (page principale), on teste les iframes...")
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                driver.switch_to.frame(iframe)
                try:
                    bouton_cookie = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(., 'Accepter et fermer')]")
                        )
                    )
                    bouton_cookie.click()
                    print("Popup cookies fermé dans une iframe.")
                    driver.switch_to.default_content()
                    break
                except TimeoutException:
                    driver.switch_to.default_content()
                    continue

        # ---------------------------------------
        # 2) Récupérer le HTML complet une fois la page chargée
        # ---------------------------------------
        html = driver.page_source
        driver.quit()

        # ---------------------------------------
        # 3) Parser avec BeautifulSoup
        # ---------------------------------------
        soup = BeautifulSoup(html, "html.parser")
        #
        base_url= "https://www.ouestfrance-immo.com"
        list_annone = soup.select_one("div.list-content__wrapper")
        list_annone = list_annone.select("a", href=True)

        try:
            for a in list_annone :
                if  a.get("href") and a.get("href").startswith("/immobilier/location/appartement/") :
                    lien_complet = urljoin(base_url , a.get("href"))
                    
        # Lancer Selenium
                    driver = webdriver.Chrome()
                    driver.maximize_window()
                    driver.get(lien_complet)

                    wait = WebDriverWait(driver, 20)

                    # ---------------------------------------
                    # 1) Fermer popup cookies "Accepter et fermer"
                    # ---------------------------------------
                    try:
                        bouton_cookie = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(., 'Accepter et fermer')]")
                            )
                        )
                        bouton_cookie.click()
                        print("Popup cookies fermé.")
                    except TimeoutException:
                        print("Popup cookies non trouvé (page principale), on teste les iframes...")
                        iframes = driver.find_elements(By.TAG_NAME, "iframe")
                        for iframe in iframes:
                            driver.switch_to.frame(iframe)
                            try:
                                bouton_cookie = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, "//button[contains(., 'Accepter et fermer')]")
                                    )
                                )
                                bouton_cookie.click()
                                print("Popup cookies fermé dans une iframe.")
                                driver.switch_to.default_content()
                                break
                            except TimeoutException:
                                driver.switch_to.default_content()
                                continue

                    # ---------------------------------------
                    # 2) Récupérer le HTML complet une fois la page chargée
                    # ---------------------------------------
                    html = driver.page_source
                    driver.quit()

                    # ---------------------------------------
                    # 3) Parser avec BeautifulSoup
                    # ---------------------------------------
                    soup = BeautifulSoup(html, "html.parser")

                    data = {}

                    # chaque ligne de caractéristiques
                    for li in soup.select("li.detail-caracteristiques__line"):
                        label_el = li.select_one(".detail-info__label span")
                        value_el = li.select_one(".detail-info__value")
                        if not label_el or not value_el:
                            continue
                    #re.search() parcourt toute la chaîne et renvoie le premier endroit où l'expression régulière correspond
                        label = re.search(r".*",label_el.get_text(strip=True)).group()
                        try :
                            value = (re.search(r'[\d\s\u00A0]+',value_el.get_text(strip=True))).group()
                            value = int(value.replace("\u202f", "").replace("\xa0€", ""))
                        except :
                            try:
                                value = value_el.get_text(strip=True)
                            except :
                                value = None
                        data[label] = value

                    try :
                        label_éco = soup.select_one('div.diagnostic-etiquette__col.diagnostic-etiquette__lettre').get_text(strip=True)
                        data["label_eco"] = label_éco
                    except :
                        data["label_eco"] = None

                        
                    for div in soup.select("div.diagnostic-etiquette__col"):

                        try :
                            lab=div.select_one(".diagnostic-etiquette__legend").get_text(strip=True)
                            try :
                                val =div.select_one(".diagnostic-etiquette__value").get_text(strip=True)#strip=True demande à BeautifulSoup de supprimer les espaces inutiles
                                val = re.search(r"\d+" , val).group()
                                data[lab] = int(val)
                            except :
                                val = None
                        except :
                            pass

                    data["Quartiers"] = quartiers
                    print(data)
                    données.append(data)
        except : 
            pass
df = pd.DataFrame(données)
df.to_csv("annonces.csv", index=False, encoding="utf-8")



