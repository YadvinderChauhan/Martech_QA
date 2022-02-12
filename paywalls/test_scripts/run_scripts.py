import subprocess
from paywalls.test_scripts import paywalls_anonymous_new
from paywalls.test_scripts import paywall_reg_logged_in_new

my_scripts = ['paywalls_anonymous_new.py', 'paywall_reg_logged_in_new.py']

for item in my_scripts:
    subprocess.run(['python', 'item'])
    print("Finished:" + item)