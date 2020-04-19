
from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_wikidata_items_for_property_value_pair(property_id, value ):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?item ?itemLabel
    WHERE { 
      ?item wdt:""" + property_id + '"' + str(value)  + '"' +   """
    }
    """
    results = get_results(endpoint_url, query)
    items  = list()
    for result in results["results"]["bindings"]:
        qid = result['item']['value']
        items.append(qid.split('/')[4])

    return(items)

def get_wikidata_item_labels_for_property_value_pair(property_id, value ):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?item ?itemLabel
    WHERE { 
      ?item wdt:""" + property_id + '"' + str(value)  + '"' +   """
    }
    """
    results = get_results(endpoint_url, query)
    items  = list()
    for result in results["results"]["bindings"]:
        qid = result['item']['value']
        items.append(qid.split('/')[4])

    return(items)
    