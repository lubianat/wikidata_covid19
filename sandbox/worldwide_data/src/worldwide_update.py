import pandas as pd
from datetime import date,timedelta

yesterday = date.today() - timedelta(days=1)
today = date.today()

yesterday_format = yesterday.strftime("%Y-%m-%d")
today_format = today.strftime("%Y-%m-%d")

def create_qs():
    countries = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv")
    wdt_items = pd.read_csv("../data/country_outbreaks.csv")

    full = pd.merge(countries, wdt_items, on="Country")

    #Most recent data seems to be from the day before
    recent = full.query("Date == @yesterday_format")

    # The following countries appear to be updated manually from more specific sources.
    idx = recent['Country'].isin(['US', 'United Kingdom', 'France', 'Sweden', 'Brazil', 'Netherlands',
                                 'China', 'Italy', 'Spain', 'Germany', 'Iran', 'Mexico', 'Argentina',
                                 'Canada', 'Spain', 'Norway', 'Portugal', 'Tunisia', 'Uruguay'])
    not_manual = recent[~idx]

    yesterday_wdt = yesterday.strftime("+%Y-%m-%dT00:00:00Z/11")
    today_wdt = today.strftime("+%Y-%m-%dT00:00:00Z/11")

    with open(f'../data/{today_format}.qs', 'w') as file:
        for index, row in not_manual.iterrows():
            print(
                  row['item'] + "|P1603|" + str(int(row['Confirmed'])) + "|P585|" + yesterday_wdt + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_wdt + "\n" +
                  row['item'] + "|P1120|" + str(int(row['Deaths'])) + "|P585|" + yesterday_wdt + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_wdt + "\n" +
                  row['item'] + "|P8010|" + str(int(row['Recovered'])) + "|P585|" + yesterday_wdt + "|S854|" + '"' +
                        "https://github.com/datasets/covid-19" + '"' +
                        "|S813|" + today_wdt + "\n",
                    file = file)

if __name__ == "__main__":
    create_qs()
