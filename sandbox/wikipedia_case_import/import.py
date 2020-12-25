
from wikidataintegrator.wdi_helpers import try_write
from wikidataintegrator import wdi_core, wdi_login
from bs4 import BeautifulSoup # library to parse HTML documents
from datetime import datetime
from getpass import getpass
import pandas as pd # library for data analysis
import requests # library to handle requests
import os

# get the response in the form of html
wikiurl="https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_death_rates"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)
soup = BeautifulSoup(response.text, 'html.parser')
casetable=soup.find('table',{'class':"wikitable"})
df=pd.read_html(str(casetable))

# convert list to dataframe
cases_df=pd.DataFrame(df[0])

local_outbreak_items = pd.read_csv("reference.csv")

reconciled = cases_df.merge(local_outbreak_items, left_on="Country", right_on="countryLabel").drop_duplicates()

# Manually fix a couple labels
template_to_label = {
    'Bahamas': 'The Bahamas',
    'China': 'mainland China',
    'Congo': 'Republic of the Congo',
    'DR Congo': 'Democratic Republic of the Congo',
    'Gambia': 'The Gambia',
    'Palestine': 'State of Palestine',
    'United States': 'United States of America' 
}

cases_df.Country = cases_df.Country.replace(template_to_label)
reconciled = cases_df.merge(local_outbreak_items, left_on="Country", right_on="countryLabel").drop_duplicates()

reconciled["Case fatality rate"] = [float(i.replace("%",""))/100 for i in reconciled["Case fatality rate"]]

reconciled["Case fatality rate"] = [round(i,3) for i in reconciled["Case fatality rate"]]

WBUSER = "TiagoLubiana"  
WBPASS = getpass(prompt='Enter your password: ')  
login = wdi_login.WDLogin(WBUSER, WBPASS)

today_in_wikidata_format = datetime.today().strftime('+%Y-%m-%dT00:00:00Z')

statements = []
for i, row in reconciled.iterrows():
    s = "Q102044164"
    p = "P527"
    o = row["item"]
    q1 = "P1120"
    oq1 = row["Deaths"]
    q2 = "P1603"
    oq2 = row["Confirmed cases"]
    q3 = "P3457"
    oq3 = row["Case fatality rate"]
    q4 = "P585"
    oq4 = today_in_wikidata_format
    r1 = "P854"
    or1 = "https://coronavirus.jhu.edu/data/mortality"
    r2 = "P143"
    or2 = "Q328"
    r3 = "P4656"
    or3 = "https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_death_rates"


    qualifier_list = [wdi_core.WDQuantity(oq1, q1,  is_qualifier=True),
                  wdi_core.WDQuantity(oq2, q2,  is_qualifier=True),
                  wdi_core.WDQuantity(oq3, q3,  is_qualifier=True), 
                  wdi_core.WDTime(oq4, q4,  is_qualifier=True)]
    
    reference_list = [[wdi_core.WDUrl(or1, r1, is_reference=True),
                  wdi_core.WDItemID(or2, r2, is_reference=True),
                  wdi_core.WDUrl(or3, r3, is_reference=True)]]
    
    statements.extend([wdi_core.WDItemID(value= o, prop_nr=p, qualifiers=qualifier_list, references=reference_list)])
    
    

item = wdi_core.WDItemEngine(wd_item_id=s, data=statements)   
item.write(login)





