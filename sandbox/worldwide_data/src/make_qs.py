#!/usr/bin/python3

"""
Generates Quickstatements commands to update COVID-19 cases on Wikidata
"""


import pandas as pd
from datetime import date, time, timedelta, datetime

import requests	


def convert_timestamp_to_time_until_now(timestamp):
    time_in_datetime_format = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")	
    diff = datetime.now() - time_in_datetime_format	
    return(diff)


def get_timestamp_of_last_edits(list_of_qids):	

    URL = "https://www.wikidata.org/w/api.php"	
    titles_for_query = "|".join(list_of_qids)	

    PARAMS = {	
        "action": "query",	
        "prop": "revisions",	
        "titles": titles_for_query,	
        "rvprop": "timestamp|user|comment|content",	
        "rvslots": "main",	
        "formatversion": "2",	
        "format": "json"	
    }	

    S = requests.Session()	
    R = S.get(url=URL, params=PARAMS)	
    DATA = R.json()	
    PAGES = DATA["query"]["pages"]	


    page_to_timestamp = {}	

    for page in PAGES:	
        page_title = page["title"]	
        timestamp_now = page["revisions"][0]['timestamp']	
        page_to_timestamp[page_title] = timestamp_now	

    return(page_to_timestamp)

def main():

    countries = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv")
    wdt_items = pd.read_csv("../data/country_outbreaks.csv")

    full_datahub_table = pd.merge(countries, wdt_items, on="Country")

    datahub_table, date = get_most_recent_entries(full_datahub_table)

    country_outbreak_items = list(datahub_table["item"])

    print("--- Retrieving outdated items ----")

    # Api only takes 50 at a time, so we have to cut it.
    table_with_outdated_items = retrieve_items_that_are_outdated(country_outbreak_items, datahub_table)


    # The following countries appear to be updated
    # manually from more specific sources.

    table_with_items_to_update = exclude_manually_updated_items(table_with_outdated_items)

    yesterday = date.today() - timedelta(days=1)
    today = date.today()

    yesterday_in_wikidata = yesterday.strftime("+%Y-%m-%dT00:00:00Z/11")
    today_in_wikidata = today.strftime("+%Y-%m-%dT00:00:00Z/11")
    
    today_format = today.strftime("%Y-%m-%d")

    with open(f'../data/{today_format}.qs', 'w') as file:
        for index, row in table_with_items_to_update.iterrows():
            print(
                  row['item'] + "|P1603|" + str(int(row['Confirmed'])) + "|P585|" + yesterday_in_wikidata + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_in_wikidata + "\n" +
                  row['item'] + "|P1120|" + str(int(row['Deaths'])) + "|P585|" + yesterday_in_wikidata + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_in_wikidata + "\n" +
                  row['item'] + "|P8010|" + str(int(row['Recovered'])) + "|P585|" + yesterday_in_wikidata + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_in_wikidata + "\n",
                    file = file)

def exclude_manually_updated_items(table_with_outdated_items):
    idx = table_with_outdated_items['Country'].isin(['US', 'United Kingdom', 'France', 'Sweden',
                                  'Brazil', 'Netherlands', 'China', 'Italy',
                                  'Spain', 'Germany', 'Iran', 'Índia', 'Mexico',
                                  'Argentina', 'Canada', 'Spain', 'Norway',
                                  'Uruguay'])

    table_with_outdated_items = table_with_outdated_items[~idx]
    return table_with_outdated_items

def retrieve_items_that_are_outdated(country_outbreak_items, datahub_table):
    # Api only takes 50 at a time, so we have to cut it.
    chunks_of_country_outbreak_items = list(get_chunks(country_outbreak_items, 50))

    outbreak_item_to_timestamp = {}
    for chunk in chunks_of_country_outbreak_items:
        outbreak_item_to_timestamp.update(get_timestamp_of_last_edits(chunk))

    datahub_table["timestamp_of_last_edit"] = datahub_table["item"].map(outbreak_item_to_timestamp)
    print(datahub_table["timestamp_of_last_edit"])
    datahub_table["time_from_last_edit_until_now"] = datahub_table["timestamp_of_last_edit"].map(convert_timestamp_to_time_until_now)

    outdated_items = datahub_table[datahub_table["time_from_last_edit_until_now"] > timedelta(hours=23)]
    return outdated_items

def get_most_recent_entries(full_datahub_table):
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in full_datahub_table["Date"]]
    most_recent_date = max(dates).strftime("%Y-%m-%d")

    datahub_table = full_datahub_table[full_datahub_table["Date"] == most_recent_date]
    return datahub_table, date

def get_chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))
            
if __name__=="__main__": 
    main()