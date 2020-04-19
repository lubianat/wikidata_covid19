import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
import re
from datetime import date, datetime

'''
This script I try to find ways of acquiring the information regarding number of recovered
cases of COVID19 in each state, still can't find a reasonable way of getting the date the 
information was uploaded in most cases. So far, I only got the full information for PE and 
RR. The rest of the states here I can only find the number, not the date.
'''

def date_to_wikidate(date):
    return datetime.strptime(date, "%d/%m/%Y").strftime("+%Y-%m-%dT00:00:00Z/11")

def RR():
    url = 'https://roraimacontraocorona.rr.gov.br/winner/public/mapa.xhtml'
    response = requests.get(url)
    soup = BS(response.content, "html.parser")
    html_table = soup.find('table', {'role': 'grid'})
    roraima = pd.read_html(str(html_table))[0]
    nrecover = roraima.iloc[-1, 2]
    date_html = soup.find('h6', {'class': 'text-muted'}).text
    match = (re.search(r'(\d+/\d+/\d+)', date_html).group(1))
    data = date_to_wikidate(match)
    return nrecover, data, url

def ES():
    es = pd.read_csv("https://bi.static.es.gov.br/covid19/MICRODADOS.csv", sep=';')
    nrecover = es.query("Evolucao == 'Cura'").shape[0]
    return nrecover, url

def PR():
    url = 'http://www.coronavirus.pr.gov.br/Campanha/Pagina/TRANSPARENCIA-Enfrentamento-ao-Coronavirus-4'
    response = requests.get(url)
    soup = BS(response.content, "html.parser")
    html_table = soup.find('table', {'class': 'col-xs-12 table-condensed table-hover table-striped'})
    parana = pd.read_html(str(html_table))[0]
    nrecover = parana.iloc[-1, 1]
    return nrecover, url

def CE():
    ce = pd.read_csv("https://indicadores.integrasus.saude.ce.gov.br/api/casos-coronavirus/export-csv", encoding="ISO-8859-1")
    ce.query("evolucaoCasoSivep == 'Cura'").codigoPaciente.nunique()
    return nrecover, url

def RO():
    url = 'http://covid19.sesau.ro.gov.br/'
    response = requests.get(url)
    soup = BS(response.content, "html.parser")
    nrecover = soup.findAll('h5')[1].text.replace('Pacientes Curados: ', '')
    return nrecover, url

def PE():
    url = 'https://www.pecontracoronavirus.pe.gov.br/'
    response = requests.get(url)
    soup = BS(response.content, "html.parser")
    nrecover = soup.findAll('h2', {'class': 'elementor-heading-title elementor-size-default'})[3].text
    date_html = soup.findAll('h2', {'class': 'elementor-heading-title elementor-size-default'})[6].text
    date_html = date_html.replace('/20', '/2020')
    data = date_to_wikidate(date_html)
    return nrecover, data, url


def get_recovery(estado):
    if estado == 'RR' :
        return RR()
    elif estado == 'ES':
        return ES()
    elif estado == 'PR':
        return PR()
    elif estado == 'CE':
        return CE()
    elif estado == 'RO':
        return RO()
    elif estado == 'PE':
        return PE()
    else:
        pass
