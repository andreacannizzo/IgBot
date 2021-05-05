# set DISPLAY to 'remote' one
import os
os.environ["DISPLAY"] = ":0"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from pickle import dump
import time
import random


# launch the browser : if images=True than browser will show images in it. returns handle to browser.
def launch_browser(path_to_chromedriver, images=True):
    if not images:
        # create browser without images
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options)
        #2del browser.get('https://www.instagram.com/')
    else:
        # create browser with images
        browser = webdriver.Chrome(path_to_chromedriver)
        #2del browser.get('https://www.instagram.com/')
    return browser


# accept cookies in popup
def cookies_accept(browser, ita):
    browser.implicitly_wait(10)
    if ita:
        browser.find_element_by_xpath("//button[text()='Accetta tutti']").click()
    else:
        browser.find_element_by_xpath("//button[text()='Accept']").click()


# logs in with account credentials specified in inputs.py file
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


# waits pop-up and click accordingly
def avoid_popup(browser, ita):
    if ita:
        WebDriverWait(browser, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Non ora"]')).click()
    else:
        WebDriverWait(browser, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Not Now"]')).click()


# insert hashtag in search bar and double press enter
def search_hashtag(browser, ita, hash_str_='#photooftheday'):
    if ita:
        search_box_xpath = "//input[@placeholder='Cerca']"
    else:
        search_box_xpath = "//input[@placeholder='Search']"
    search_box = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, search_box_xpath)))
    search_box.send_keys(hash_str_)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)


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


# click first pic of the recents
def click_first_pic(browser, first_rec, second_rec, third_rec):
    try:
        first_image = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, first_rec)))
        time.sleep(5)
        first_image.click()
    except Exception:
        # print(f'post in {first_rec} not found')
        try:
            first_image = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, second_rec)))
            time.sleep(5)
            first_image.click()
        except Exception:
            # print(f'post in {second_rec} not found')
            try:
                first_image = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, third_rec)))
                time.sleep(5)
                first_image.click()
            except Exception:
                print(f'post in {third_rec} not found')


def like_if_its_ok(browser, number, like_xpath):
    like = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, like_xpath)))
    color = like.get_property("innerHTML")
    if "#262626" in color:
        time.sleep(random.uniform(3, 6))
        like.click()
        time.sleep(random.uniform(3, 6))
        return 1
    else:
        time.sleep(random.uniform(3, 5))
        return 0


def skip_to_next_one(browser, next_path):
    time.sleep(10)
    browser.find_element_by_xpath(next_path).click()


# Returns string containing account's handle of current viewed post
def account_handle(browser, handle_xpath):
    handle_handle = WebDriverWait(browser, 1).until(
        EC.visibility_of_element_located((By.XPATH, handle_xpath)))
    return handle_handle.text


# Insert new line in Log file (da finire)
def append_entry_(browser, account_handle_str):
    new_entry = {"action": "liked",
                 "account_handle": account_handle_str,
                 "time": datetime.now(),
                 "post_URL": browser.current_url}
    with open("LogFilesPickle", "ab+") as file:
        dump(new_entry, file)

