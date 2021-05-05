from selenium.common.exceptions import TimeoutException
from inputs import *
from definitions import *
import sys
import time
from datetime import datetime

# save log files and time informations
original_stdout = sys.stdout
start_time = time.strftime("%Y_%m_%d-%H_%M_%S")
start_timer = datetime.now()

# Open a new Log file in a directory dependently if it's running on the Mac or the Raspberry Pi
if mac:
    file_name = "/Users/andreacannizzo/WorkSpace/IgBot/LogFiles/" + start_time + ".txt"
else:
    file_name = "/home/pi/WorkSpace/IgBot/LogFiles/" + start_time + ".txt"
f = open(file_name, "w")
f.close()

# open a browser and get its handle
browser = launch_browser(path_to_chromedriver, False)
# go to instagram
browser.get('https://www.instagram.com/')
# accept cookies
cookies_accept(browser, ita)
# log in with accounts credentials
login(browser, username_str, password_str)
# avoid 'save credentials' popup and then 'notifications' popup, the same function works for both
avoid_popup(browser, ita)
avoid_popup(browser, ita)

# create session history variables
total_aim_of_likes = 0
total_viewed_posts = 0
total_liked = 0

# starts session
for hash_i in hash_str:

    # print(f"searching for {hash_i} posts")
    search_hashtag(browser, ita, hash_i)
    click_first_pic(browser, first_recent, second_recent, third_recent)

    # create other session and utility variables
    # tryings = number of times IgBot skips to a new post if the previous isn't active
    # skip = counter of how many times in a row there are already-liked posts
    liked = 0
    total = 0
    tryings = 0
    result_of_LIIO = 0
    skip = 0

    # starting from the most recent post there is no need to change the xpath of the 'next_post' bc they are all equal
    while (liked < target_of_likes) and (skip < max_skip):
        try:
            # get account's handle of current post viewed (works but not useful now)
            # ig_handle_str = account_handle(browser, handle_xpath)
            # result_of_LIIO = 1 if liked successfully, 0 if not liked because already liked
            result_of_LIIO = like_if_its_ok(browser, liked, like_xpath)
            # update liked session variable
            liked += result_of_LIIO
            # go to next post
            browser.find_element_by_xpath(next_path).click()
            # whether it was a like or not the total amount of posts viewed increases by one
            total += 1
            # if it's been a like than the counter of already-liked posts is reset to 0
            if result_of_LIIO == 1:
                skip = 0
            else:
                skip += 1
        except TimeoutException:
            if tryings == max_tryings:
                print(f'Images did not load after {max_tryings} attempts')
                browser.close()
                exit()
            # when post doesn't load IgBot tries to skip to the next one max_tryings times
            skip_to_next_one(browser, next_path)
            tryings += 1

    # display local outcome
    with open(file_name, 'a') as f:
        sys.stdout = f
        print(f"- {hash_i} posts, target of likes = {target_of_likes}, likes = {liked}, total viewed = {total}")
    total_aim_of_likes += target_of_likes
    total_viewed_posts += total
    total_liked += liked

# saves time when finishes session and display global outcome
time_elapsed = datetime.now() - start_timer
with open(file_name, 'a') as f:
    sys.stdout = f
    print(f"total target = {total_aim_of_likes}, total viewed = {total_viewed_posts}, total liked = {total_liked}")
    print(f"total time (hh:mm:ss) = {format(time_elapsed)}")

# displays outcome in python console
sys.stdout = original_stdout
with open(file_name, 'r') as f:
    print(f.read())

# close browser and exit
browser.close()
