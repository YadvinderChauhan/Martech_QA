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

# 2. Open a new browser session, go to The Telegraph website and maximize the window
driver.get(
	"https://www.telegraph.co.uk/?martech_preprod=true&qauxtestingpaywalls=true"
)
driver.maximize_window()
wait_variable = W(driver, wait_time_out)
time.sleep(3)
# Delete a cookie with name 'consentUUID'
driver.delete_cookie("consentUUID")

# Adds the cookie into current browser context
driver.add_cookie({"name": "consentUUID", "value": "2dfe1a9d-f1d7-45a9-a78b-3f964097af30"})

driver.refresh()
time.sleep(3)

# 4. Read each test url from the list, and create a list
with open("../test_data/paywall_urls.txt", "r") as urlFile:
	urls_list = []
	for url in urlFile:
		urls_list.append(url.strip())

	# 5. open each article one by one by reading the list
	for url in urls_list:
		print(url)
		driver.get(url)
		time.sleep(2)
		driver.execute_script("window.scroll(0, 1100)")

# 12. Close the session
driver.close()
driver.quit()