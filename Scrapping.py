
""" Bibliothèques """

import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By





# Configurer le répertoire de téléchargement
download_folder = os.path.expanduser("~/Downloads")
prefs = {"download.default_directory": download_folder}







###############################################################################
########################### Scrapping calories   ##############################
###############################################################################


# Configurer Selenium WebDriver pour Chrome avec options de téléchargement
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)


# URL de la page à scraper
url = "https://ourworldindata.org/grapher/daily-per-capita-caloric-supply?tab=table"


driver.get(url)

time.sleep(5)# Attendre que la page se charge complètement

############################## Gérer la fenêtre de cookies ##############################
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I agree')]"))
    )
    accept_cookies_button.click()
except Exception as e:
    print("Fenêtre de cookies non trouvée ou autre problème :", e)

# Attendre que la page se charge complètement après avoir cliqué sur les cookies
time.sleep(5)



########################### Télécharger le fichier des données ########################### 
try:
    end_marker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='handle endMarker']"))
    )
    ActionChains(driver).click_and_hold(end_marker).move_by_offset(-200, 0).release().perform()  

    # Attendre que la page se mette à jour
    time.sleep(5)

    # Cliquer sur le bouton de téléchargement
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))
    )
    download_button.click()

    # Attendre que le bouton "Full data (CSV)" apparaisse et cliquer dessus
    csv_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Full data (CSV)')]"))
    )
    csv_button.click()


    time.sleep(10)

except Exception as e:
    print("Erreur lors du téléchargement du fichier CSV :", e)


driver.quit()


######################## Récupérer le fichier télécharger ###########################


csv_file_path = os.path.join(download_folder, "daily-per-capita-caloric-supply.csv")

if os.path.exists(csv_file_path):

    df = pd.read_csv(csv_file_path)
    
    # Filtrer les années spécifiées
    df_calories = df[df['Year'].isin([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])]
    
    df_calories.drop(columns=['Code'], inplace=True)

    # Renommer la colonne 'Daily calorie supply per person' en 'calories'
    df_calories.rename(columns={'Daily calorie supply per person': 'calories'}, inplace=True)

 













###############################################################################
########################### Scrapping diabetes   ##############################
###############################################################################




# Configurer Selenium avec le driver Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
# Accéder à la page web
url = "https://ourworldindata.org/grapher/diabetes-prevalence?tab=table"
driver.get(url)

# Attendre le chargement complet du tableau
driver.implicitly_wait(10)

# Extraire le tableau
table = driver.find_element(By.TAG_NAME, 'table')
headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]

rows = []

for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
    cells = row.find_elements(By.TAG_NAME, 'td')
    rows.append([cell.text for cell in cells])

# Créer un DataFrame pandas
df_diabetes_2021 = pd.DataFrame(rows, columns=headers)

# DataFrame diabètes 2014
first_url = "https://ourworldindata.org/grapher/diabetes-prevalence-who-gho?tab=table&time="
last_url = "..latest#explore-the-data"
df_diabetes = pd.DataFrame()

i = 2000
url = first_url + str(i) + last_url
driver.get(url)
driver.implicitly_wait(10)
table = driver.find_element(By.TAG_NAME, 'table')
headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
rows = []
for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
    cells = row.find_elements(By.TAG_NAME, 'td')
    rows.append([cell.text for cell in cells])

df_diabetes_temp = pd.DataFrame(rows, columns=headers)
selected_column = df_diabetes_temp.iloc[:, [0,1]]
df_diabetes = selected_column
for i in range(2001, 2015):
    url = first_url + str(i) + last_url
    driver.get(url)
    driver.implicitly_wait(10)
    table = driver.find_element(By.TAG_NAME, 'table')
    headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
    rows = []
    for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        rows.append([cell.text for cell in cells])

    df_diabetes_temp = pd.DataFrame(rows, columns=headers)
    selected_column = df_diabetes_temp.iloc[:, 1]

    df_diabetes = pd.concat([df_diabetes, selected_column], axis=1)


driver.quit()


df_filtered = df_diabetes_2021[df_diabetes_2021['Country/area'].isin(df_diabetes['Country/area'])]

merged_df = pd.merge(df_diabetes, df_filtered, on='Country/area', how='inner')



for column in merged_df.columns:
    if column != 'Country/area':
        merged_df[column] = merged_df[column].str.rstrip('%')
merged_df['2014'] = pd.to_numeric(merged_df['2014'], errors='coerce')
merged_df['2021'] = pd.to_numeric(merged_df['2021'], errors='coerce')
df_interpolated = merged_df[['Country/area']].copy()

# Loop through each country
for country in merged_df['Country/area'].unique():

    value_2014 = merged_df.loc[merged_df['Country/area'] == country, '2014'].values[0]
    value_2021 = merged_df.loc[merged_df['Country/area'] == country, '2021'].values[0]

    years = np.arange(2015, 2021)
    interpolated_values = np.interp(years, [2014, 2021], [value_2014, value_2021])


    for year, value in zip(years, interpolated_values):
        df_interpolated.loc[df_interpolated['Country/area'] == country, str(year)] = value


for year in range(2015, 2021):
    merged_df[str(year)] = df_interpolated[str(year)]


year_columns = [str(year) for year in range(2000, 2022)]  # Adjust the range if needed
# Reorder columns
merged_df = merged_df[['Country/area'] + year_columns]


merged_df.rename(columns={'Country/area': 'Entity'}, inplace=True)
df_diabetes = pd.melt(merged_df, id_vars=['Entity'], var_name='Year', value_name='diabetes')















###############################################################################
########################### Scrapping Obesite   ##############################
###############################################################################





options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)


url = "https://ourworldindata.org/grapher/share-of-adults-defined-as-obese?tab=table"


driver.get(url)

time.sleep(5)

# Gérer la fenêtre de cookies
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I agree')]"))
    )
    accept_cookies_button.click()
except Exception as e:
    print("Fenêtre de cookies non trouvée ou autre problème :", e)


time.sleep(5)


try:
    end_marker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='handle endMarker']"))
    )
    ActionChains(driver).click_and_hold(end_marker).move_by_offset(-300, 0).release().perform() 


    time.sleep(5)


    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))
    )
    download_button.click()


    csv_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Full data (CSV)')]"))
    )
    csv_button.click()


    time.sleep(10)  

except Exception as e:
    print("Erreur lors du téléchargement du fichier CSV :", e)


driver.quit()


csv_file_path = os.path.join(download_folder, "share-of-adults-defined-as-obese.csv")

if os.path.exists(csv_file_path):
    # Lire le fichier CSV téléchargé avec Pandas
    df = pd.read_csv(csv_file_path)
    
    
    # Filtrer les années spécifiées
    df_filtered = df[df['Year'].isin([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016])]
    
    # Pivoter le DataFrame pour avoir les années comme colonnes
    df_pivot_obesite = df_filtered.pivot(index='Entity', columns='Year', values='Prevalence of obesity among adults, BMI >= 30 (crude estimate) (%) - Sex: both sexes - Age group: 18+  years')

    # Renommer les colonnes pour une meilleure lisibilité
    df_pivot_obesite.columns = [str(col) for col in df_pivot_obesite.columns]

    # Ajouter des colonnes pour les années manquantes (2017 à 2021) avec des valeurs NaN
    years_to_add = [2017, 2018, 2019, 2020, 2021]
    for year in years_to_add:
        df_pivot_obesite[str(year)] = np.nan

    # Réordonner les colonnes pour avoir les années dans l'ordre
    df_pivot_obesite = df_pivot_obesite[sorted(df_pivot_obesite.columns, key=int)]


    # Interpoler les valeurs manquantes
    df_pivot_obesite = df_pivot_obesite.interpolate(method='linear', axis=1)
    
    df_pivot_obesite.reset_index(inplace=True)
    
    df_obesity = pd.melt(df_pivot_obesite, id_vars=['Entity'], var_name='Year', value_name='obesity')



df_diabetes['Year'] = df_diabetes['Year'].astype(int)
df_obesity['Year'] = df_obesity['Year'].astype(int)
df_calories['Year'] = df_calories['Year'].astype(int)
df_combined = pd.merge(pd.merge(df_diabetes, df_obesity, on=['Entity', 'Year']), df_calories, on=['Entity', 'Year'])

df_combined.to_csv('tous_data.csv', index=False)
