import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from webdriver_manager.chrome import ChromeDriverManager
#######################################################################
# User defined functions
from utilities import extract_icid, extract_url

#######################################################################
wait_time_out = 15
# 1. Install the Chrome driver at the run time.
# Create an object of service class and pass the chrome driver installation instance
s = Service(ChromeDriverManager().install())

# Initiate the driver service object
driver = webdriver.Chrome(service=s)

# 1. Read the urls from the source file and creating a list.
with open("../test_data/overlay_urls.txt", "r") as file:
	urls_list = file.read().split('\n')

	# 2. Read each test url from the list and open a new browser session.
	for url in urls_list:
		print(url)
		driver.get(url)
		driver.maximize_window()
		time.sleep(2)
###################################################################
#########   notes
#martech.info.displayed.modal
#martech.info.activitiesDetails.1.CUS-1725--aem-hard-paywall.campaignName
#################################################################
