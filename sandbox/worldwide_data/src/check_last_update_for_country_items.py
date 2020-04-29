#!/usr/bin/python3

"""
# Checking last updates for country items

Besides manually checking which page have local updates, it is interesting to have an automatic view of which pages have been updated recently. 

We do not want (initially, at least) to re enter numbers for pages that were recently updated.

lubianat, adapted from mediawiki https://www.mediawiki.org/wiki/API:Revisions#Example_1:_Get_revision_data_of_several_pages


"""



"""
    get_pages_revisions.py

    MediaWiki API Demos
    Demo of `Revisions` module: Get revision data with content for pages
    with titles [[API]] and [[Main Page]]

    MIT License
"""

import requests

"""
    get_timestamp_of_last_edits

    list_of_qids: A list of QIDs for the pages you want to get the time stamp
    
    returns a dictionary with QIDs and associated timestamps.
"""


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