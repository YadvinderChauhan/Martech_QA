
from utilities import extract_icid, extract_url

cta_url = "https://secure.telegraph.co.uk/customer/secure/checkout/?productId=nyytq4zthbvwsoliojugwyzzmyzha3dt&offerId=freetrial-digital-month-RP001&campaignId=038A&ICID=primary_paywalls_digital_subscribe_paymentpage_anon&redirectTo=https%3A%2F%2Fwww.telegraph.co.uk%2Fpolitics%2F2022%2F02%2F04%2Fcongratulated-bbc-inviting-unvaccinated-question-time-might%2F%3Fmartech_preprod%3Dtrue%26qamanylive%3Dtrue%26aem-hard-paywall%3Dfalse%26engaged%3Dfalse%26non-engaged%3Dfalse"

cta_icid = extract_icid.get_icid(cta_url)
print(cta_icid)

new_cta_url = extract_url.get_url(cta_url)
print(new_cta_url)

print(get)
'''
# write the URLs and the ICIDs to the text file.




with open("../icids/urls_and_icids.txt", mode="a") as icidsFile:
	icidsFile.write("\nNew Paywall")
	icidsFile.write("\nCTA url: " + new_cta_url)
	icidsFile.write("\nCTA ICID: " + cta_icid + "\n")
print('CTA urls and the ICIDs saved in the file')





# 12. Close the session
driver.close()
driver.quit()
'''
