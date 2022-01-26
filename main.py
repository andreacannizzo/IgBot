from selenium.common.exceptions import TimeoutException
from inputs import *
from definitions import *
import chromedriver_autoinstaller
import os


# auto download latest chromedriver if mac then open a browser and get its handle
# TODO fix the chromedriver_autoinstaller for Rasp
auto_chromedriver = chromedriver_autoinstaller.install()
browser = launch_browser(auto_chromedriver, False)

if os.path.exists("Clients_Files/" + username_str + "/cookies_file"):
    LOAD_cookie(browser, username_str)
else:
    SAVE_cookies(browser, username_str, password_str)

# work parameters
target_of_likes = 30
max_tryings = 5
max_skip = 18

for hash_i in hash_str:

    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get("https://www.instagram.com/explore/tags/"+hash_i)
    click_first_pic(browser)
    liked = 0
    like_result = 0
    skip = 0
    tryings = 0
    while (liked < target_of_likes) and (skip < max_skip):
        try:
            # If there is a restriction of actions IgBot detects it and stops
            try:
                # TODO substitute right english version
                browser.find_element_by_xpath("//button[text()='Segnala un problema']").click()
                print("Instagram detected weird actions")
                browser.close()
                exit()
            except:
                pass
            like_result = like_it(browser)
            liked += like_result
            next(browser)
            if like_result == 1:
                add_like(browser, hash_i, username_str)
                skip = 0
            else:
                skip += 1
        except TimeoutException:
            if tryings == max_tryings:
                print(f'Images did not load after {max_tryings} attempts')
                browser.close()
                exit()
            # when post doesn't load IgBot tries to skip to the next one max_tryings times
            next(browser)
            tryings += 1

    browser.close()
    browser.switch_to.window(browser.window_handles[0])


# close browser and exit
browser.close()
exit()
