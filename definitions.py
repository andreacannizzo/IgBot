from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import re


def lunch_browser(path_to_chromedriver, images=True):
    if not images:
        # create browser without images
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options)
        browser.get('https://www.instagram.com/')
    else:
        # create browser with images
        browser = webdriver.Chrome(path_to_chromedriver)
        browser.get('https://www.instagram.com/')
    return browser


def cookies_accept(browser):
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//button[text()='Accetta']").click()


def login(browser, username_str, password_str):
    username = browser.find_element_by_name('username')
    username.clear()
    username.send_keys(username_str)
    password = browser.find_element_by_name('password')
    password.clear()
    password.send_keys(password_str)
    # confirm
    submit = browser.find_element_by_tag_name('form')
    submit.submit()


def avoid_popups(browser):
    # wait save credentials pop-up and click not now
    WebDriverWait(browser, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Non ora"]')).click()
    # wait notifications request and click not now
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//button[text()='Non ora']").click()


def search_hashtag(browser, hash_str_='#photooftheday'):
    # insert hashtag in search bar and double press enter
    search_box_xpath = "//input[@placeholder='Cerca']"
    search_box = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, search_box_xpath)))
    search_box.send_keys(hash_str_)
    # store number of posts for relative hashtag
    tag_xpath = "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div/div/div[2]/span/span"
    tag_xpath_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, tag_xpath)))
    number_of_posts_str = tag_xpath_button.get_property("innerHTML")
    number_of_posts = int(re.sub("[^\d]", "", number_of_posts_str))
    print(f"total number of posts for {hash_str_} = {number_of_posts}")
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    return number_of_posts


def scroll_down_function(browser, nr_of_scroll):
    scroll_pause_time = 0.5
    for i in range(nr_of_scroll):
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


def click_first_pic(browser):
    first_of_populars = "//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]"
    first_of_recents = "//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]"
    first_image = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, first_of_recents)))
    time.sleep(5)
    first_image.click()


def like_if_its_ok(browser, number):
    like_xpath = '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button'
    like = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, like_xpath)))
    color = like.get_property("innerHTML")
    if "#262626" in color:
        time.sleep(random.uniform(2, 5))
        like.click()
        print(number + 1)
        time.sleep(random.uniform(2, 5))
        return 1
    else:
        time.sleep(random.uniform(3, 4))
        return 0


def back_n_forth(browser):
    time.sleep(10)
    print("go back")
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[1]").click()
    time.sleep(10)
    print("go forth")
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
