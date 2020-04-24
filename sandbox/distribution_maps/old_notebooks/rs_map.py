import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
import geopandas as gpd
import matplotlib.pyplot as plt

''' 
My idea is to maybe unify map creation based on functions similar to the ones in this script. 
Maybe we can manage to do that, even though city-based data is very irregular.
'''

def get():
    url = 'http://ti.saude.rs.gov.br/covid19/'
    response = requests.get(url)
    soup = BS(response.content, "html.parser")
    html_table = soup.find('table')
    return(html_table)

def transform(html_table):
    rs = pd.read_html(str(html_table))[0]
    rs['Municipio'] = rs['Municipio'].str.replace(r'\d+\.\s', '').str.upper()
    mapa_dos_municipios = gpd.read_file("./estados_shapes/unzipped/43MUE250GC_SIR.shp")
    mapa_dos_municipios.columns = ['Municipio', 'idMunicipio', 'geometry']
    map_conf = pd.merge(mapa_dos_municipios, rs, on='Municipio', how='left')
    map_conf["Confirmados"] = map_conf["Confirmados"].fillna(0).astype(float)
    map_conf["casos_categorizados"] = pd.cut(map_conf["Confirmados"],
                                                    bins = [-1,1, 10,50,500, 1000],
                                                   labels = ["0", "1-10", "11-50", "51-500", ">500"])
    return(map_conf)

def plot_map(mapa):
    fig, ax = plt.subplots()
    ax = mapa.plot(column='casos_categorizados',
                             categorical=True, 
                             legend=True, 
                             figsize=(10,6),
                             markersize=46,
                             cmap = "Reds",
                             edgecolor='k',
                             linewidth=0.1,
                             ax=ax);
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0., 0., 0.3, 0.32))
    plt.savefig("casos_rs" + ".png", dpi = 300)

def main():
    html_table = get()
    map_conf = transform(html_table)
    plot_map(map_conf)

if __name__ == "__main__":
    main()
