from definitions import *
from inputs import *
import chromedriver_autoinstaller
import os
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
# auto download latest chromedriver if mac then open a browser and get its handle
# TODO fix the chromedriver_autoinstaller for Rasp
auto_chromedriver = chromedriver_autoinstaller.install()
browser = launch_browser(auto_chromedriver, False)

if os.path.exists("Clients_Files/" + username_str + "/cookies_file"):
    LOAD_cookie(browser, username_str)
else:
    SAVE_cookies(browser, username_str, password_str)

put_likes(browser)

# close browser and exit
browser.close()
exit()