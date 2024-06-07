from selenium import webdriver
import pandas as pd
import requests
import csv

##########################################################################################################################################################################
#                                                                                                                                                                        #
#    SCRIPT EXTRACTION TOP DE CONTIBUTION PAR LANGAGE SUR GITHUB SELON LA LISTE DES COMPANIES DANS LE 20 DES REVENUS 2023 (source wiki) SUR LE SITE OSCI                 #
#                                                                                                                                                                        #
##########################################################################################################################################################################


# Liste des entreprises dans le top 20 par revenu (source wiki et Projet_extraction_top_wiki.py)
LISTE = ["Apple", "Google", "Samsung", "Microsoft", "Meta", "Huawei", "Sony", "Tencent", 
         "LG Electronics", "Intel", "Hewlett Packard Enterprise", "Accenture", "IBM"]



driver = webdriver.Chrome()
base_url = 'https://opensourceindex.io/?company='

# Créer une liste pour stocker les données
data = []

try:
    for company in LISTE:
        url = base_url + company
        
        driver.get(url)
        driver.implicitly_wait(10)  
        
        # Récupérer les éléments
        Company = driver.find_element_by_class_name('ranking-table-drilldown-card-company').text
        Nb_contributors = driver.find_element_by_class_name('ranking-table-drilldown-card-total').text
        

        lang_elements = driver.find_elements_by_class_name('ranking-table-drilldown-card-lang')
        Nom_languages = [lang.text.strip() for lang in lang_elements]
        

        data.append([Company, Nb_contributors, Nom_languages])
    
finally:
    driver.quit()

# Créer un DataFrame pandas à partir des données
df = pd.DataFrame(data, columns=['Company', 'Nb_contributors', 'Nom_languages'])

