from state_scripts import get_recovery
from datetime import date
import pandas as pd

'''
Script to generate QS for the number of recovered cases. See state_scripts.py for further
explanation.
'''

dic = pd.read_csv("../dicionario.csv")

def get_qs():
    for index, row in dic.iterrows():
        if row['estado'] == "RR" or row['estado'] == "PE":
            print(
                row['item'] + "|P8010|" + get_recovery(row['estado'])[0] + "|P585|" + get_recovery(row['estado'])[1] +
                "|S854|" + '"' + get_recovery(row['estado'])[2] + '"' +
                "|S813|" + date.today().strftime("+%Y-%m-%dT00:00:00Z/11")
                 )
        else:
            pass

if __name__ == "__main__":
    get_qs()
