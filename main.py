from selenium.common.exceptions import TimeoutException
# private variables and information are stored in inputs.py file
#       web_site = 'string'
#       username_str = 'string'
#       password_str = 'string'
#       hash_str = '#string'
#       like2put = number
from inputs import *
from definitions import *


browser = lunch_browser(path_to_chromedriver, False)
cookies_accept(browser)
login(browser, username_str, password_str)
avoid_popups(browser)
search_hashtag(browser, hash_str)
time.sleep(5)
scroll_down(browser)
click_first_pic(browser)


# create variables that counts liked posts, total viewed, tryings and max number of tryings
liked = 0
total = 0
tryings = 0
max_tryings = 3


# starting from the most recent post there is no need to change the xpath of the 'next_post' because they are all equal
while liked < target_of_likes:
    try:
        liked += like_if_its_ok(browser, liked)
        browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
        total += 1
    except TimeoutException:
        if tryings == max_tryings:
            print(f'image did not load after {max_tryings} attempts')
            browser.close()
            exit()
        back_n_forth(browser)
        tryings += 1


# display outcome
print(f'target of likes = {target_of_likes}')
print(f'likes = {liked}')
print(f'total viewed = {total}')

# close browser and exit
browser.close()
