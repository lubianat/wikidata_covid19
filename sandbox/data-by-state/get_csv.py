from selenium import webdriver
import os
import glob
import time
from datetime import date

'''
This script is used to acquire the latest csv file from Min. da saúde. 
Since they don't provide an easy link to directly read it in pandas nor an API, 
the solution I found was creating a bot browser instance to click their button, download the csv and 
change the name of the newest downloaded file to match the day it was retrived.
'''

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
#File pathing for download dir could be improved
profile.set_preference('browser.download.dir', '~/Documentos/Wikidata/wikidata_covid19/sandbox/data-by-state/Saude_csvs/')
#Don't ask permission to download
profile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

browser = webdriver.Firefox(profile)
browser.get("https://covid.saude.gov.br/")

time.sleep(5) #This line is necessary for bad internet service such as the one I have, but unecessary otherwise.

browser.find_element_by_xpath('/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button').click()
time.sleep(10) #To let it finish downloading before closing instance.
browser.close()

#Change name of the latest file in directory
list_of_files = glob.glob('./Saude_csvs/*csv') 
latest_file = max(list_of_files, key=os.path.getctime)
current = latest_file
newname = f"./Saude_csvs/{str(date.today())}.csv"
os.rename(current,newname)
