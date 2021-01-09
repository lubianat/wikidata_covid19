
import pywikibot
from datetime import datetime


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


# Update Wikidata via pywikibot


site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

for i, row in reconciled.iterrows():
    print(row["item"])
    item = pywikibot.ItemPage(repo, row["item"])
    item.get() #Fetch all page data, and cache it.

    # Add number of deaths

    ## Value --> death count

    deaths_claim = pywikibot.Claim(repo, u'P1120') # Adding number of deaths (P1120)
    deaths_claim.setTarget(pywikibot.WbQuantity(row["Deaths"])) #Set the target value in the local object.
    item.addClaim(deaths_claim, summary=u'Adding death count from template.')


    ## Qualifier --> date 

    qualifier = pywikibot.Claim(repo, u'P585') # Adding qualifier of point in time (P585)
    today = datetime.today() #Date today
    target = pywikibot.WbTime(year=int(today.strftime("%Y")), month=int(today.strftime("%m")), day=int(today.strftime("%d")))
    qualifier.setTarget(target)
    deaths_claim.addQualifier(qualifier, summary=u'Adding date.')


    ## Source --> Wikipedia template URL
    wiki_url = pywikibot.Claim(repo, u'P4656') # reference URL (P854)
    wiki_url.setTarget("https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_death_rates")
    
     ## Source --> Imported from English Wikipedia
    ref = pywikibot.Claim(repo, u'P143') #stated in (P248)
    ref.setTarget(pywikibot.ItemPage(repo, 'Q328'))

    ## Source --> Retrieved today
    retrieved = pywikibot.Claim(repo, u'P813') #retrieved (P813). Data type: Point in time
    retrieved_target = pywikibot.WbTime(year=int(today.strftime("%Y")), month=int(today.strftime("%m")), day=int(today.strftime("%d"))) #retrieved -> %DATE TODAY%. Example retrieved -> 29.11.2020
    retrieved.setTarget(retrieved_target) #Inserting value

    deaths_claim.addSources([ref,wiki_url, retrieved], summary=u'Adding sources.')

    break
