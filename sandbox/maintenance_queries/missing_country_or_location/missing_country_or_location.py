# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Maintenance queries related to COVID-19
#
# In this notebook I try to analyse some of the maintenance queries available [here](https://www.wikidata.org/wiki/Wikidata:WikiProject_COVID-19/Queries#Maintenance_queries), with some of my modifications to facilitate the process and fix at least some of the missing properties
# %% [markdown]
# ### Missing location
# Query I used:
# %% [markdown]
# ```
# SELECT ?item ?itemLabel ?itemDescription ?country ?countryLabel ?valid_in_place ?valid_in_placeLabel
# {
# 	?item wdt:P31 wd:Q3241045 .
# 	?item wdt:P361+ wd:Q81068910 .
#     ?item p:P31 ?instance .
#     OPTIONAL {?item wdt:P17 ?country}
#     OPTIONAL {?instance pq:P3005 ?valid_in_place}
# 	MINUS { ?item p:P276 [] }
# 	SERVICE wikibase:label { bd:serviceParam wikibase:language "pt-br,en". }
# }
# ```
# %% [markdown]
# Ended up just extracting the table from the website because parsing the JSON would've been too much of a hassle for me.

# %%
import pandas as pd


# %%
missing_location = pd.read_csv("./missing_location.csv")
missing_location


# %%
missing_location = missing_location.iloc[4:, :]


# %%
missing_location


# %%
idx = missing_location["itemLabel"].str.contains("Pandemia de COVID-19 na cidade")
brazilian_cities = missing_location[idx]
brazilian_cities


# %%
for index, row in brazilian_cities.iterrows():
    print(
        row["item"]
        + "|Len|"
        + '"'
        + f"COVID-19 pandemic in the city of {row['valid_in_placeLabel']}"
        + '"\n'
        + row["item"]
        + "|P361|"
        + "Q86597695"
        + "\n"
        + row["item"]
        + "|P17|"
        + "Q155"
        + "\n"
        + row["item"]
        + "|P276|"
        + row["valid_in_place"]
        + "\n"
    )


# %%
missing_other = missing_location[idx == False]
missing_other_valid = missing_other[missing_other["valid_in_place"].notnull()]
missing_other_valid


# %%
missing_other_valid = missing_other_valid[:-1]
for index, row in missing_other_valid.iterrows():
    pandemic_in = row["itemLabel"].replace(
        "2020 coronavirus pandemic in ", "viral pandemic in "
    )
    print(
        row["item"]
        + "|Den|"
        + '"'
        + pandemic_in
        + '"\n'
        + row["item"]
        + "|P276|"
        + row["valid_in_place"]
        + "\n"
    )

# %% [markdown]
# ### Missing country
# %% [markdown]
# These items are missing country statements, but not location, so I retrieve the country from the location statement.

# %%
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?item ?itemLabel ?itemDescription ?country ?countryLabel{
	?item wdt:P31 wd:Q3241045 . 
	?item wdt:P361+ wd:Q81068910 .   
    ?item wdt:P276 ?location .
    ?location wdt:P17 ?country .
	MINUS { ?item p:P17 [] }
	SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)


# %%
dic = {
    "item": [],
    "itemLabel": [],
    "itemDescription": [],
    "country": [],
    "countryLabel": [],
}
for result in results["results"]["bindings"]:
    a = result["item"]["value"]
    dic["item"].append(a.split("/")[4])
    b = result["itemLabel"]["value"]
    dic["itemLabel"].append(b)
    try:
        c = result["itemDescription"]["value"]
        dic["itemDescription"].append(c)
    except:
        dic["itemDescription"].append(None)
    d = result["country"]["value"]
    dic["country"].append(d.split("/")[4])
    e = result["countryLabel"]["value"]
    dic["countryLabel"].append(e)


# %%
missing_country = pd.DataFrame(dic)


# %%
# Dropping for Sevastopol since it's a disputed territory
missing_country = missing_country[:26]
for index, row in missing_country.iterrows():
    pandemic_in = row["itemLabel"].replace(
        "2020 coronavirus pandemic in ", "viral pandemic in "
    )
    print(
        row["item"]
        + "|Den|"
        + '"'
        + pandemic_in
        + '"\n'
        + row["item"]
        + "|P17|"
        + row["country"]
        + "\n"
    )

