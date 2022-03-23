import subprocess
import time
from paywalls.test_scripts import paywalls_anonymous
from paywalls.test_scripts import paywall_reg_logged_in

my_scripts = ['paywalls_anonymous.py', 'paywall_reg_logged_in.py']

for item in my_scripts:
    subprocess.run(['python', 'item'])
    time.sleep(3)
    print("Finished:" + item)