from selenium.common.exceptions import TimeoutException
from inputs import *
from definitions import *
import chromedriver_autoinstaller

auto_chromedriver = chromedriver_autoinstaller.install()
browser = launch_browser(auto_chromedriver, False)
browser.get('https://www.instagram.com/')
avoid_popup(browser, "Accept All")
login(browser, username_str, password_str)
avoid_popup(browser, "Not Now")
avoid_popup(browser, "Not Now")
browser.execute_script("window.open('');")
browser.switch_to.window(browser.window_handles[1])
browser.get("https://www.instagram.com/explore/tags/moda")
click_first_pic(browser, first_recent, second_recent, third_recent)
like_if_its_ok(browser, like_xpath)
