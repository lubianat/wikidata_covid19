import pandas as pd
from datetime import date,datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import requests

def get_dataframe(api_url, id_municipio=''):
    api_url = api_url + '?'
    if(id_municipio != ''):
        api_url = '{}idMunicipio={}&'.format(api_url, id_municipio)

    result = requests.get(api_url)
    result = result.json()
    result = pd.DataFrame.from_dict(result)

    if(id_municipio != ''):
        result.insert(0, 'idMunicipio', id_municipio)

    return result

def build_table():
    api_endpoint = 'https://indicadores.integrasus.saude.ce.gov.br/api/coronavirus/qtd-por-municipio'

    qtd_por_municipios  = get_dataframe(api_endpoint).query(
        "tipo == 'Confirmado'"
    ).loc[:,['municipio', 'qtdConfirmado']]

    mapa_dos_municipios = gpd.read_file("../../../estados_shapes/unzipped/23MUE250GC_SIR.shp")
    mapa_dos_municipios.columns = ['municipio', 'idMunicipio', 'geometry']
    map_conf = pd.merge(mapa_dos_municipios, qtd_por_municipios, on='municipio', how='left')

    map_conf["qtdConfirmado"] = map_conf["qtdConfirmado"].fillna(0)

    map_conf["casos_categorizados"] = pd.cut(map_conf["qtdConfirmado"],
                                                    bins = [-1,1, 10,50,500,1000, 100000000],
                                                   labels = ["0", "1-10", "11-50", "51-500","501-1000", ">1000"])
    return map_conf

def plot_map(map_conf):
    fig, ax = plt.subplots()
    ax = map_conf.plot(column='casos_categorizados',
                             categorical=True,
                             legend=True,
                             figsize=(100,6),
                             markersize=46,
                             cmap = "Reds",
                             edgecolor='k',
                             linewidth=0.1,
                             ax=ax);
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0., 0., 0.2, 0.2))
    plt.savefig("casos_CE" + ".png", dpi = 300)

def main():
    map_conf = build_table()
    plot_map(map_conf)

if __name__=="__main__":
    main()
