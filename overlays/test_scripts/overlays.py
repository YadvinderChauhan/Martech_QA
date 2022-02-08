from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import datetime
import time

# 1. Read the urls from the source file and creating a list.
with open("../test_data/overlay_urls.txt", "r") as file:
	urls_list = file.read().split('\n')

	# 2. Read each test url from the list and open a new browser session.
	for url in urls_list:
		# 3. Install the Chrome driver at the run time.
		# Create an object of service class and pass the chrome driver installation instance
		s = Service(ChromeDriverManager().install())

		# Initiate the driver service object
		driver = webdriver.Chrome(service=s)

		# 4. Go to the test article page
		print(url)
		driver.get(url)
		driver.maximize_window()
		time.sleep(2)

		# 5. Get the channel name from the url after retrieving and splitting the path.
		obj = urlparse(url)
		path = obj.path
		path_list = path.split("/")
		channel_name = path_list[1]  # channel name would be used to name the screenshots later.
		# time.sleep(2)

		# 6. Take the screenshot of the pay wall and save it after the channel name retrieved in section 5 above
		# and save in the screenshots directory named
		date_stamp = str(datetime.datetime.now()).split('.')[0]
		new_date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
		if channel_name == '':
			new_channel_name = 'home_portal'
			#driver.save_screenshot("../screenshots/" + new_channel_name + ".png")
			driver.save_screenshot("../screenshots/" + "anon_" + new_channel_name + new_date_stamp + ".png")
		else:
			#driver.save_screenshot("../screenshots/" + channel_name + ".png")
			driver.save_screenshot("../screenshots/" + "anon_" + channel_name + new_date_stamp + ".png")
		print("screenshot saved successfully")
		time.sleep(2)
		'''##########################################
		Take the screenshot of the pay wall and save it in the screenshots directory
        #    named after the channel name retireved in section 5 above.
        date_stamp = str(datetime.datetime.now()).split('.')[0]
        new_date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
        driver.save_screenshot("../screenshots/" + "anon_" + channel_name + new_date_stamp + ".png")
        print("Screenshot saved successfully")


		
		-------------------
		# 7. Switch to the overlay
		overlay = driver.find_element(By.CSS_SELECTOR, ".martech-modal-component.martech-sale-overlay")
		if overlay:
			overlay.click()
			print('overlay clicked')
			time.sleep(2)
			dismiss = driver.find_element(By.CSS_SELECTOR, ".martech-modal-component__close")
			dismiss.click()
			print('overlay dismissed')
			time.sleep(2)
		else:
			print('Overlay not found')
		time.sleep(5)'''
		##########################################
		# 12. Close the session
		driver.close()
		driver.quit()
