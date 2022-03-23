import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from webdriver_manager.chrome import ChromeDriverManager
#######################################################################
# User defined functions
from utilities import get_overlay as go
from utilities import extract_icid, extract_url

#######################################################################
wait_time_out = 15
# 1. Install the Chrome driver at the run time.
# Create an object of service class and pass the chrome driver installation instance
s = Service(ChromeDriverManager().install())

# Initiate the driver service object
driver = webdriver.Chrome(service=s)

# 2. Open a new browser session, go to The Telegraph website and maximize the window
driver.get("https://www.telegraph.co.uk/?martech_preprod=true")
driver.maximize_window()
wait_variable = W(driver, wait_time_out)
time.sleep(3)

# 3. Delete a cookie with name 'consentUUID'
driver.delete_cookie("consentUUID")

# 4. Add the cookie into current browser context
driver.add_cookie({"name": "consentUUID", "value": "2dfe1a9d-f1d7-45a9-a78b-3f964097af30"})

driver.refresh()
time.sleep(3)

# 5. Read the urls from the source file and creating a list.
with open("../test_data/inclusions.txt", "r") as file:
#with open("../test_data/inclusions.txt", "r") as file:
	urls_list = file.read().split('\n')

	# 6. Read each test url from the list and open a new browser session.
	for url in urls_list:
		print(url)
		driver.get(url)
		time.sleep(2)

		# 7. Check if the page should display the modal
		modal_expected = driver.execute_script('return martech.info.displayed.modal')

		# 8. Get the details of all the activities that are delivered on the page.
		activities_list = driver.execute_script('return martech.info.activitiesDetails')
		time.sleep(2)

		# 9. Get the name of the overlay that is expected on the page.
		overlay = go.get_overlay(activities_list)
		time.sleep(2)
		if modal_expected != True:
			print('No overlay expected on this page')
			time.sleep(1)
			#break
		else:
			print(overlay + ' is expected on the page')

			# 10. Click on the displayed overlay and dismiss it.
			displayed_overlay = driver.find_element(By.CLASS_NAME,'martech-modal-component').click()
			time.sleep(2)
			#print(displayed_overlay)
			#print('Switched to ' + displayed_overlay)
			dismiss_overlay = driver.find_element(By.CLASS_NAME, 'martech-modal-component__close').click()
			time.sleep(1)
			print('Overlay dismissed')
			time.sleep(2)

# 12. Close the session
driver.close()
driver.quit()