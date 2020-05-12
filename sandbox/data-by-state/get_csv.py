from selenium import webdriver
import os
import glob
import time
from datetime import date, timedelta
import argparse

'''
This script is used to acquire the latest csv file from Min. da saúde. 
Since they don't provide an easy link to directly read it in pandas nor an API, 
the solution I found was creating a bot browser instance to click their button, download the csv and 
change the name of the newest downloaded file to match the day it was retrived.
'''

# Arguments via command line give a bit more flexibility

# Current implementation requires as input the full path ending with "/"
# It can be improved for usability.
parser = argparse.ArgumentParser(description='Argparse to pass commands via command line')
parser.add_argument("--downdir",
                    default='/home/jvfe/Documentos/Wikidata/wikidata_covid19/sandbox/data-by-state/Saude_csvs/',
                    help="The directory to download the files to")
parser.add_argument("--topen",
                    default=5,
                    help="Time to load the page in selenium")
parser.add_argument("--tclose",
                    default=10,
                    help="Time to close the page in selenium")
arguments = parser.parse_args()

time_to_open = int(arguments.topen)
time_to_close = int(arguments.tclose)
download_directory = arguments.downdir


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
#File pathing for download dir could be improved
profile.set_preference('browser.download.dir', download_directory)
#Don't ask permission to download
profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


browser = webdriver.Firefox(profile)
browser.get("https://covid.saude.gov.br/")
time.sleep(time_to_open) #This line is necessary for bad internet service such as the one I have, but unecessary otherwise.
browser.find_element_by_xpath('/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button').click()
time.sleep(time_to_close) #To let it finish downloading before closing instance.
browser.close()


#Change name of the latest file in directory
#list_of_files = glob.glob(download_directory + '*csv') 
#print(list_of_files)
#latest_file = max(list_of_files, key=os.path.getctime)
#current = latest_file

#As of 21, april, the website changed the naming convention of the csvs to not be random anymore
today = date.today().strftime("%Y%m%d")

current = os.path.join(download_directory, f'DT_PAINEL_COVIDBR_{today}.xlsx')
newname = os.path.join(download_directory, f"{str(date.today())}.csv")
os.rename(current,newname)
