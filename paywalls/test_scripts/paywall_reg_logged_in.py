import datetime
import time
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from webdriver_manager.chrome import ChromeDriverManager

wait_time_out = 15

# 1. Install the Chrome driver at the run time.
# Create an object of service class and pass the chrome driver installation instance
s = Service(ChromeDriverManager().install())

# Initiate the driver service object
driver = webdriver.Chrome(service=s)

# 2. Open a new browser session, go to The Telegraph website and maximize the window
driver.get(
	"https://www.telegraph.co.uk/?martech_preprod=true&qamanylive=true&aem-hard-paywall=false&engaged=false&non-engaged=false"
)

driver.maximize_window()
wait_variable = W(driver, wait_time_out)
time.sleep(5)

# 3. Get geo location and check if cookie banner should get delivered.
# The parameter "country_with_cookie_banner" is used to determine if the cookie consent should be displayed or not.
# in the console if country_with_cookie_banner == false, that means the country location won't see the cookie banner
# cookie_consent is used to establish if the cookie-consent has already been given.

cookie_banner_country = driver.execute_script('return martech.visitor.country_with_cookie_banner')
cookie_consent_given = driver.execute_script('return martech.visitor.cookie_consent')
geo_location = driver.execute_script('return martech.visitor.geo_location') # This will form part of the screenshot name.

if cookie_consent_given == True or cookie_banner_country == False:
	print('Cookie banner not expected.')

elif cookie_banner_country == True:
	# 4. Check if the Cookie Banner exists, and accept if yes.
	try:
		iframe = driver.find_element(By.ID, "sp_message_iframe_607910")
		if iframe.is_displayed():
			driver.switch_to.frame(iframe)
			print("Switched to cookie banner")
			accept_button = driver.find_element(By.CSS_SELECTOR,
			                                    "button.message-component.message-button.no-children.focusable.cmp-cta-accept.sp_choice_type_11"
			                                    )
			accept_button.click()
			print("Telegraph Cookies Accepted")
			time.sleep(5)
		else:
			print("Info: No cookie banner displayed.")
	except Exception as e:
		print(e)

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

driver.get("https://www.telegraph.co.uk/politics/2022/02/06/treasury-blocks-boris-johnsons-plan-clear-nhs-backlog"
           "/?martech_preprod=true&qamanylive=true&aem-hard-paywall=false&engaged=false&non-engaged=false")
time.sleep(7)
driver.execute_script("window.scroll(0, 2500)")
time.sleep(5)


# 5. Read each test url from the list, and create a list
with open("../test_data/paywall_urls.txt", "r") as urlFile:
	urls_list = urlFile.read().split('\n')
	# print(urls_list)

	# 6. open each article one by one by reading the list
	for url in urls_list:
		print(url)
		driver.get(url)
		time.sleep(5)

		# 7. Identify the content type to establish which paywall on the page is expected.
		# ====================================================================================================================================
		# old paywall gets displayed where content_type is "story" or "live" or "video" or "longform"  and channel is 'travel' or 'property'
		# gallery paywall gets displayed where content_type is gallery
		# new paywall gets displayed where content_type is "story" or "live" or "video" or "longform"  and page_renderer: "articleRenderer"

		content_type = driver.execute_script('return martech.visitor.content_type')
		channel_name = driver.execute_script('return martech.visitor.channel')
		page_renderer = driver.execute_script('return martech.visitor.page_renderer')

		# 8. Scroll down the page to maximize the paywall if required
		if content_type == 'gallery':
			pass
		else:
			driver.execute_script("window.scroll(0, 1100)")
			time.sleep(3)

		# 9. Define the page variables - used to identify which paywall is expected
		is_old_paywal = (
					                content_type == "story" or content_type == "live" or content_type == "video" or content_type == "longform") and (
					                channel_name == 'travel' or channel_name == 'property')
		is_gallery_paywall = (content_type == "gallery")
		is_new_paywal = not (is_old_paywal and page_renderer == "articleRenderer") and (
					content_type == "story" or content_type == "live" or content_type == "video" or content_type == "longform") and not (
			is_gallery_paywall)

		if is_old_paywal:
			# extract the CTA url
			cta_url = driver.find_element(By.CLASS_NAME, "martech-paywall__cta-main").get_attribute("href")
			# print(cta_url)
			head, sep, tail = cta_url.partition('&redirectTo')
			new_cta_url = head
			# extract the ICID from the CTA url
			query = urlparse(cta_url).query
			path_list = parse_qs(query)['ICID']
			cta_icid = path_list[0]
			print('ICID=' + cta_icid)

			# write the URLs and the ICIDs to the text file.
			with open("../icids/urls_and_icids.txt", mode="a") as icidsFile:
				icidsFile.write("\n" + geo_location.upper() + ": LOGGED IN REGISTRANT")
				icidsFile.write("\nOld Paywall")
				icidsFile.write("\nCTA url: " + new_cta_url)
				icidsFile.write("\nCTA ICID: " + cta_icid + "\n")

		elif is_gallery_paywall:
			# extract the CTA url
			cta_url = driver.find_element(By.CLASS_NAME, "martech-paywall__cta-main").get_attribute("href")
			# print(cta_url)
			head, sep, tail = cta_url.partition('&redirectTo')
			new_cta_url = head
			# extract the ICID from the CTA url
			query = urlparse(cta_url).query
			path_list = parse_qs(query)['ICID']
			cta_icid = path_list[0]
			print('ICID=' + cta_icid)

			# write the URLs and the ICIDs to the text file.
			with open("../icids/urls_and_icids.txt", mode="a") as icidsFile:
				icidsFile.write("\nGallery Paywall")
				icidsFile.write("\nCTA url: " + new_cta_url)
				icidsFile.write("\nCTA ICID: " + cta_icid + "\n")

		elif is_new_paywal:
			# extract the CTA url
			cta_url = driver.find_element(By.CLASS_NAME, "martech-new-paywall-mechanism__button").get_attribute("href")
			# print(cta_url)
			head, sep, tail = cta_url.partition('&redirectTo')
			new_cta_url = head
			# extract the ICID from the CTA url
			query = urlparse(cta_url).query
			path_list = parse_qs(query)['ICID']
			cta_icid = path_list[0]
			print('ICID=' + cta_icid)
			# write the URLs and the ICIDs to the text file.
			with open("../icids/urls_and_icids.txt", mode="a") as icidsFile:
				icidsFile.write("\nNew Paywall")
				icidsFile.write("\nCTA url: " + new_cta_url)
				icidsFile.write("\nCTA ICID: " + cta_icid + "\n")
		print('CTA urls and the ICIDs saved in the file')

		# 10. Saving the screenshots.
		date_stamp = str(datetime.datetime.now()).split('.')[0]  # gives the date_stamp as 2022-01-21 11:30:11
		new_date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_"
		                                                                        )  # gives the new_date_stamp as 2021_12_06_12_49_17
		if channel_name == '':
			new_channel_name = 'home_portal'
			driver.save_screenshot("../screenshots/" + geo_location.upper() + "_REG_" + new_channel_name + new_date_stamp + ".png")
		else:
			driver.save_screenshot("../screenshots/" + geo_location.upper() + "_REG_" + channel_name + new_date_stamp + ".png")
	print("screenshot saved successfully")
	time.sleep(3)

# 12. Close the session
driver.close()
driver.quit()
