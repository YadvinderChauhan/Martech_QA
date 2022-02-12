
paywall_files = {"paywall_urls": "../paywalls/test_data/paywall_urls.txt",
                  "login_credentials": "../paywalls/test_data/login_credentials.txt",
                  "urls_and_icids": "../paywalls/icids/urls_and_icids.txt"
                  }

def file_location(key):
    try:
        return paywall_files[key]
    except KeyError:
        print('Key not found')
