import urllib.request
from bs4 import BeautifulSoup
import lxml.html


# 4. Read each test url from the list, and create a list
with open("../web_scraping/test_data/paywall_urls.txt", "r") as urlFile:
	urls_list = urlFile.read().split('\n')
	for url in urls_list:
		print(url)
		soup = BeautifulSoup(urllib.request.urlopen(url).read())
		#print(soup)
		paywall = soup.find('@class_name','martech-new-paywall-mechanism')
		print(paywall)
