from selenium.common.exceptions import TimeoutException
# private variables and information are stored in inputs.py file
#       web_site = 'string'
#       username_str = 'string'
#       password_str = 'string'
#       hash_str = '#string'
#       like2put = number
from inputs import *
from definitions import *
import math
import random


browser = lunch_browser(path_to_chromedriver, False)
cookies_accept(browser)
login(browser, username_str, password_str)
avoid_popups(browser)

for hash_i in hash_str:
    print(f"searching for {hash_i} posts")
    number_of_posts = search_hashtag(browser, hash_i)
    max_number_of_scroll_to_bottom = math.floor(number_of_posts/100)
    random_scrolls = random.randint(1, max_number_of_scroll_to_bottom)
    print(f"total number of scroll to proceed = {random_scrolls}")
    scroll_down_function(browser, random_scrolls)
    click_first_pic(browser)

    # create variables that counts liked posts, total viewed, tryings, result of like function and number
    # of total posts skipped in a row
    liked = 0
    total = 0
    tryings = 0
    result_of_LIIO = 0
    skip = 0

    # starting from the most recent post there is no need to change the xpath of the 'next_post' bc they are all equal
    while (liked < target_of_likes) and (skip > max_skip):
        try:
            result_of_LIIO = like_if_its_ok(browser, liked)
            liked += result_of_LIIO
            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
            total += 1
            skip += result_of_LIIO - 1
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
