import requests
from bs4 import BeautifulSoup
import csv

##########################################################################################################################################################################
#                                                                                                                                                                        #
#    SCRIPT EXTRACTION DE LA LISTE DES COMPANIES LES PLUS GRANDES PAR REVENUE (SOURCE WIKIPEDIA)                                                                         #
#                                                                                                                                                                        #
##########################################################################################################################################################################



url = "https://en.wikipedia.org/wiki/List_of_largest_technology_companies_by_revenue"


response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')


tables = soup.find_all('table', {'class': 'wikitable'})


h2_element = soup.find('span', {'id': '2023_list'}).find_parent('h2')


table_2023list = None
table_position = -1


for i, table in enumerate(tables):
    if h2_element.find_next('table') == table:
        table_2023list = table
        table_position = i + 1 
        break


table_2023list_headers = [header.text.strip() for header in table_2023list.find_all('th')]


table_2023list_rows = []
if table_2023list.find('tbody'):
    for row in table_2023list.find('tbody').find_all('tr'):
        table_2023list_rows.append([val.text.strip() for val in row.find_all('td')])
else:
    for row in table_2023list.find_all('tr'):
        table_2023list_rows.append([val.text.strip() for val in row.find_all('td')])


with open('2023list_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(table_2023list_headers)
    writer.writerows(table_2023list_rows)