import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
import geopandas as gpd
import requests

'''
I believe a good way of organizing the code will be creating classes for the different
kinds of map creation we've been using. Here I aggregate all maps I've made from scraping
tables in state websites into instances of the same class.
'''

class MapScraper:
    def __init__(self, name, url, shapefile):
        self.url = url
        self.shapefile = shapefile
        self.name = name

    def get(self):
        response = requests.get(self.url)
        soup = BS(response.content, "html.parser")
        html_table = soup.find('table')
        return(html_table)

    def transform(self, html_table):
        estado = pd.read_html(str(html_table))[0]
        # This rename line is very ugly but it looks necessary to deal with the states I got.
        estado.rename({'Cidade': 'Municipio', 'Nome do município': 'Municipio', 'Confir-mados':'Confirmados'}, axis=1, inplace=True)
        estado.replace('-', 0, inplace=True)
        estado['Municipio'] = estado['Municipio'].str.replace(r'\d+\.\s', '').str.upper()
        mapa_dos_municipios = gpd.read_file(self.shapefile)
        mapa_dos_municipios.columns = ['Municipio', 'idMunicipio', 'geometry']
        map_conf = pd.merge(mapa_dos_municipios, estado, on='Municipio', how='left')
        map_conf["Confirmados"] = map_conf["Confirmados"].fillna(0).astype(float)
        map_conf["casos_categorizados"] = pd.cut(map_conf["Confirmados"],
                                                        bins = [-1,1, 10,50,500, 1000, 10000],
                                                       labels = ["0", "1-10", "11-50", "51-500", ">500", ">1000"])
        return(map_conf)

    def plot_map(self, map_conf):
        fig, ax = plt.subplots()
        ax = map_conf.plot(column='casos_categorizados',
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
        plt.savefig(f"casos_{self.name}" + ".png", dpi = 300)

    def calls(self):
        html_table = self.get()
        map_conf = self.transform(html_table)
        self.plot_map(map_conf)


ma = MapScraper(
    url="https://www.corona.ma.gov.br/",
    shapefile="./shapefiles/21MUE250GC_SIR.shp",
    name = "MA")

rr = MapScraper(
    url="https://roraimacontraocorona.rr.gov.br/winner/public/mapa.xhtml",
    shapefile="./shapefiles/14MUE250GC_SIR.shp",
    name = "RR")

#rs = MapScraper(
#    url="http://ti.saude.rs.gov.br/covid19/",
#    shapefile="../../../estados_shapes/unzipped/43MUE250GC_SIR.shp",
#    name = "RS")


ma.calls()

rr.calls()

#rs.calls()

