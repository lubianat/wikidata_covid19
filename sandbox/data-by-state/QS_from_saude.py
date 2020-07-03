import requests
import pandas as pd
from datetime import date, timedelta

# This script is to be run after get_csv.py

# Setting global variables for today and yesterday
yesterday = date.today() - timedelta(days=1)
today = date.today()

# Makes a request to get the url of the most recent data

def get_data():
    headers = {"X-Parse-Application-Id" : "unAFkcaNDeXajurGB7LChj8SgQYS2ptm"}
    req = requests.get('https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral', 
              params = headers)
    url = req.json()['results'][0]['arquivo']['url']
    return(url)

# The following function reads the table, filters it
# and merges it with the local dictionary of Qids.

def transform(table):
    nacional = pd.read_excel(table)
    yesterday_saude = yesterday.strftime("%Y-%m-%d")
    nacional_hoje = nacional.query("data == @yesterday_saude")
    dic = pd.read_csv("./dicionario.csv")
    full = pd.merge(nacional_hoje, dic, on="estado")
    #This seems to be the most effective way to get state-level data, not city-level.
    only_estados = full[full['codmun'].isnull()]
    return(only_estados)

# The following function generates the QS from the transformed
# table, then prints it to stdout.
# This function could use some improvement, such as integration with the QS api.

def generate_qs(full):
    yesterday_wdt = yesterday.strftime("+%Y-%m-%dT00:00:00Z/11")
    today_wdt = today.strftime("+%Y-%m-%dT00:00:00Z/11")
    for index, row in full.iterrows():
        print(
      row['item'] + "|P1603|" + str(int(row['casosAcumulado'])) + "|P585|" + yesterday_wdt + "|S854|" + '"' + "https://covid.saude.gov.br/" + '"' +
            "|S813|" + today_wdt + "\n" +
      row['item'] + "|P1120|" + str(int(row['obitosAcumulado'])) + "|P585|" + yesterday_wdt + "|S854|" + '"' + "https://covid.saude.gov.br/" + '"' +
            "|S813|" + today_wdt  
        )

# All function calls
def main():
    today_data = get_data()
    full = transform(today_data)
    generate_qs(full)

if __name__=="__main__":
    main()
