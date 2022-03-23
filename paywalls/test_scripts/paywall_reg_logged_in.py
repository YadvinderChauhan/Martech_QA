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
time.sleep(2)
driver.find_element(By.ID, "login-button").click()
print('Login successful')
time.sleep(3)

driver.get("https://www.telegraph.co.uk/politics/2022/02/04/congratulated-bbc-inviting-unvaccinated-question-time"
           "-might/?martech_preprod=true&qauxtestingpaywalls=true")
time.sleep(3)
driver.execute_script("window.scroll(0, 2000)")
time.sleep(2)


# 6. Read each test url from the list, and create a list
with open("../test_data/paywall_urls.txt", "r") as urlFile:
	urls_list = []
	for url in urlFile:
		urls_list.append(url.strip())

	# 7. open each article one by one by reading the list
	for url in urls_list:
		print(url)
		driver.get(url)
		time.sleep(3)

		# 8. Identify the content type to establish which paywall on the page is expected.
		content_type = driver.execute_script('return martech.visitor.content_type')
		channel_name = driver.execute_script('return martech.visitor.channel')
		page_renderer = driver.execute_script('return martech.visitor.page_renderer')

		# 9. Scroll down the page to maximize the paywall if required
		if content_type == 'gallery':
			pass
		else:
			driver.execute_script("window.scroll(0, 1100)")
			time.sleep(3)

		# 10. Define the page variables - used to identify which paywall is expected
		is_old_paywal = (content_type == "story" or content_type == "live" or content_type == "video" or content_type == "longform")\
		                and (channel_name == 'travel' or channel_name == 'property')

		is_gallery_paywall = (content_type == "gallery")

		is_new_paywal = not (is_old_paywal and page_renderer == "articleRenderer") \
		                and (content_type == "story" or content_type == "live" or content_type == "video" or content_type == "longform") \
		                and not (is_gallery_paywall)

		# 11. Establish the expected paywall and retrieve the CTA URL, and Login URL and their ICIDs.
		if is_old_paywal:
			paywall_cta_url = driver.find_element(By.CLASS_NAME, "martech-paywall__cta-main").get_attribute("href")
			old_paywall_cta_url = extract_url.get_url(paywall_cta_url)
			old_paywall_cta_icid = extract_icid.get_icid(paywall_cta_url)

		elif is_gallery_paywall:
			cta_url = driver.find_element(By.CLASS_NAME, "martech-paywall__cta-main").get_attribute("href")
			gallery_cta_url = extract_url.get_url(cta_url)
			gallery_cta_icid = extract_icid.get_icid(gallery_cta_url)

		elif is_new_paywal:
			cta_url = driver.find_element(By.CLASS_NAME, "martech-new-paywall-mechanism__button").get_attribute("href")
			new_paywall_cta_url = extract_url.get_url(cta_url)
			new_paywall_cta_icid = extract_icid.get_icid(new_paywall_cta_url)

		# 11. Save each screenshot.
		date_stamp = str(datetime.datetime.now()).split('.')[0]  # gives the date_stamp as 2022-01-21 11:30:11
		new_date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_"
		                                                                        )  # gives the new_date_stamp as 2021_12_06_12_49_17
		if channel_name == '':
			new_channel_name = 'home_portal'
			driver.save_screenshot("../screenshots/" + geo_location.upper() + "_REG_" + new_channel_name + new_date_stamp + ".png")
		else:
			driver.save_screenshot("../screenshots/" + geo_location.upper() + "_REG_" + channel_name + new_date_stamp + ".png")
		print("Screenshot saved successfully")
	time.sleep(3)

	# 12. Write the URLs and the ICIDs to the text file.
	with open("../icids/cta_urls_and_icids.txt", mode="a") as icidsFile:
		# Old paywall
		icidsFile.write("\n\n" + geo_location.upper() + ": REGISTRANT - LOGGED IN")
		icidsFile.write("\nOld Paywall")
		icidsFile.write("\nCTA url: " + old_paywall_cta_url)
		icidsFile.write("\nCTA ICID: " + old_paywall_cta_icid)

		# Gallery
		icidsFile.write("\n\nGallery Paywall")
		icidsFile.write("\nCTA url: " + gallery_cta_url)
		icidsFile.write("\nCTA ICID: " + gallery_cta_icid)

		# # New Paywall
		# icidsFile.write("\n\nNew Paywall")
		# icidsFile.write("\nCTA url: " + new_paywall_cta_url)
		# icidsFile.write("\nCTA ICID: " + new_paywall_cta_icid)

	print('CTA urls and the ICIDs saved in the file')

# 13. Close the session
driver.close()
driver.quit()