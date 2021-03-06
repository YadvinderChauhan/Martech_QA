
from datetime import datetime, timedelta
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
today = datetime.today()
sixty_days_ago = str(today - timedelta(days=60))

#two_months_ago = datetime.strptime(sixty_days_ago, '%m/%d/%y')
print(sixty_days_ago_ago)
'''
b = datetime.strptime('10/15/13', '%m/%d/%y')

print 'a' if a > b else 'b' if b > a else 'tie'


wait_time_out = 15
# 1. Install the Chrome driver at the run time.
# Create an object of service class and pass the chrome driver installation instance
s = Service(ChromeDriverManager().install())

# Initiate the driver service object
driver = webdriver.Chrome(service=s)

# 2. Open a new browser session, go to The Telegraph website and maximize the window
driver.get(
	"https://www.telegraph.co.uk/news/2018/05/20/royal-wedding-guests-moved-tears-prince-charles-speech-darling/?martech_preprod=true&qauxtestingpaywalls=true"
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
content_type = driver.execute_script('return martech.visitor.content_type')
article_published = driver.execute_script('martech.visitor.article_first_published')
article_published_date = datetime.strptime(article_published, '%m/%d/%y')

if article_published_date < two_months_ago:
	print('yes it is')
else:
	print('No')
	time.sleep(2)


driver.close()
driver.quit()
'''