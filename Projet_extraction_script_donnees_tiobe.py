from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import matplotlib.pyplot as plt
from selenium import webdriver
from datetime import datetime
import pandas as pd
import requests
import csv
import json

##########################################################################################################################################################################
#                                                                                                                                                                        #
#          SCRIPT EXTRACTION DONNEES DE CLASSEMENT DES LANGAGE INFORMATIQUE SELON LE GRAPHIQUE SUR LA PAGE TIOBE.COM                                                     #
#                                                                                                                                                                        #
##########################################################################################################################################################################



url = 'https://www.tiobe.com/tiobe-index/'
responce = requests.get(url)

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)

links = driver.find_elements(By.XPATH,"//body//section//div//article//script")

script_tableau = links[1].get_attribute('innerHTML')

driver.close()

import re


donnees_brutes = script_tableau

# Définition de l'expression régulière pour extraire chaque bloc de données
pattern = r"\{name\s*:\s*'([^']*)',\s*data\s*:\s*\[([\w\W]+?)\]\}"


donnees_par_nom = {}

# Recherche des correspondances dans les données brutes
matches = re.findall(pattern, donnees_brutes)

if matches:

    for match in matches:
        # Extraction du nom
        nom = match[0]
        
        # Extraction des données sous forme de liste de tuples (date, valeur)
        donnees = []
        data_string = match[1]
        data_pattern = r"\[Date\.UTC\((\d+),\s*(\d+),\s*(\d+)\),\s*([\d.]+)\]"
        for data_match in re.finditer(data_pattern, data_string):
            date = tuple(map(int, data_match.groups()[:3]))
            valeur = float(data_match.group(4))
            donnees.append((date, valeur))
        
        # Stockage des données dans le dictionnaire
        donnees_par_nom[nom] = donnees



# Selection des données par date 
donnees_python = donnees_par_nom['Python']
donnees_python = donnees_python[231:]
donnees_c = donnees_par_nom['C']
donnees_c = donnees_c[231:]
donnees_cplusplus = donnees_par_nom['C++']
donnees_cplusplus = donnees_cplusplus[231:]
donnees_java = donnees_par_nom['Java']
donnees_java = donnees_java[231:]
donnees_javascript = donnees_par_nom['JavaScript']
donnees_javascript = donnees_javascript[231:]
donnees_go = donnees_par_nom['Go']
donnees_go = donnees_go[133:]
donnees_cdiz = donnees_par_nom['C#']
donnees_cdiz = donnees_cdiz[231:]


# Création du dataframe ordonné
df_python = pd.DataFrame(donnees_python, columns=['date', 'Python'])
df_python['date'] = df_python['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_python['date'] = pd.to_datetime(df_python['date'])

df_c = pd.DataFrame(donnees_c, columns=['date', 'C'])
df_c['date'] = df_c['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_c['date'] = pd.to_datetime(df_c['date'])

df_cplusplus = pd.DataFrame(donnees_cplusplus, columns=['date', 'C++'])
df_cplusplus['date'] = df_cplusplus['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_cplusplus['date'] = pd.to_datetime(df_cplusplus['date'])

df_java = pd.DataFrame(donnees_java, columns=['date', 'Java'])
df_java['date'] = df_java['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_java['date'] = pd.to_datetime(df_java['date'])

df_javascript = pd.DataFrame(donnees_javascript, columns=['date', 'Javascript'])
df_javascript['date'] = df_javascript['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_javascript['date'] = pd.to_datetime(df_javascript['date'])

df_go = pd.DataFrame(donnees_go, columns=['date', 'GO'])
df_go['date'] = df_go['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_go['date'] = pd.to_datetime(df_go['date'])

df_cdiz = pd.DataFrame(donnees_cdiz, columns=['date', 'C#'])
df_cdiz['date'] = df_cdiz['date'].apply(lambda x: f"{x[0]}-{x[1]+1:02d}-{x[2]:02d}")
df_cdiz['date'] = pd.to_datetime(df_cdiz['date'])

dfs = [df_python, df_c, df_cplusplus, df_java, df_javascript, df_go, df_cdiz]

df = pd.concat([df.set_index('date') for df in dfs], axis=1)

df.to_csv('evolution_popularite_langage.csv')


# Réorganiser les données dans un format long (melt)
df2 = df.reset_index()
df_melted = df2.melt(id_vars=['date'], var_name='Nom_langage', value_name='popularité')

# Filtrer les données pour décembre 2023
december_2023_data = df_melted[df_melted['date'] == '2023-12-04']
december_2023_data.to_csv('december_2023_data.csv')