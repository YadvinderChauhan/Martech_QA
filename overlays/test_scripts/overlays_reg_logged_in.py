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
	"https://www.telegraph.co.uk/?martech_preprod=true&qaoverlyengagedoverlay=true&qaoverlyengagedoverlay=false"
)
driver.maximize_window()
wait_variable = W(driver, wait_time_out)
#time.sleep(1)

# Delete a cookie with name 'consentUUID'
driver.delete_cookie("consentUUID")

# Adds the cookie into current browser context
driver.add_cookie({"name": "consentUUID", "value": "2dfe1a9d-f1d7-45a9-a78b-3f964097af30"})

driver.refresh()

# 3. Get geo location and check if cookie banner should get delivered.
# cookie_banner_country = driver.execute_script('return martech.visitor.country_with_cookie_banner')
# cookie_consent_given = driver.execute_script('return martech.visitor.cookie_consent')
geo_location = driver.execute_script('return martech.visitor.geo_location') # This will form part of the screenshot name.

# 4. Read the email ID and the password for the test account from the text file.
with open("../test_data/login_credentials.txt", "r") as userFile:
	account_list = userFile.read().split(',')
	email_id = account_list[0]
	password = account_list[1]

# 5. Now login as a registrant user from the navbar
driver.switch_to.default_content()
driver.find_element(By.LINK_TEXT, "Log in").click()  # Login option on the navbar clicked
print('Log in option clicked')

driver.find_element(By.ID, "email").send_keys(email_id)
driver.find_element(By.ID, "login-button").click()
time.sleep(2)
driver.find_element(By.ID, "password").send_keys(password)
# time.sleep(2)
driver.find_element(By.ID, "login-button").click()
print('Login successful')
time.sleep(3)

driver.get("https://www.telegraph.co.uk/politics/2022/02/04/congratulated-bbc-inviting-unvaccinated-question-time"
           "-might/?martech_preprod=true&qamanylive=true&aem-hard-paywall=false&general-soft=false&qaoverlyengagedoverlay=false")
time.sleep(7)
driver.execute_script("window.scroll(0, 2000)")
time.sleep(5)


# 1. Read the urls from the source file and creating a list.
#with open("../test_data/exclusions.txt", "r") as file:
with open("../test_data/inclusions.txt", "r") as file:
	urls_list = file.read().split('\n')

	# 2. Read each test url from the list and open a new browser session.
	for url in urls_list:
		print(url)
		driver.get(url)
		driver.maximize_window()
		time.sleep(5)

# 12. Close the session
driver.close()
driver.quit()