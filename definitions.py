# set DISPLAY to 'remote' one
import os
os.environ["DISPLAY"] = ":0"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import pandas as pd
import time
import random
import pickle
from inputs import *


def launch_browser(path_to_chromedriver, images=True, headless=True):
    chrome_options = webdriver.ChromeOptions()
    if images:
        chrome_options.add_experimental_option("prefs", {"intl.accept_languages": 'en,en_US'})
    else:
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,
                                                         'intl.accept_languages': 'en,en_US'})
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1000,700")
    browser = webdriver.Chrome(path_to_chromedriver, options=chrome_options)
    return browser


def avoid_popup(browser, text_of_button):
    try:
        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='" + text_of_button + "']"))).click()
    except:
        print("There's no popup with a <" + text_of_button + "> button")


def login(browser, username_str, password_str):
    username = browser.find_element(By.NAME, 'username')
    username.clear()
    username.send_keys(username_str)
    password = browser.find_element(By.NAME, 'password')
    password.clear()
    password.send_keys(password_str)
    # confirm
    submit = browser.find_element(By.TAG_NAME, "form")
    submit.submit()


def save_cookie(browser, username_str):
    if os.path.exists("Clients_Files/" + username_str):
        path = "Clients_Files/" + username_str + "/cookies_file"
    else:
        os.makedirs("Clients_Files/" + username_str)
        path = "Clients_Files/" + username_str + "/cookies_file"
    with open(path, 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def SAVE_cookies(browser, username_str, password_str):
    browser.get('https://www.instagram.com/')
    avoid_popup(browser, "Allow essential and optional cookies")
    time.sleep(5)
    login(browser, username_str, password_str)
    time.sleep(5)
    avoid_popup(browser, "Save Info")
    time.sleep(3)
    save_cookie(browser, username_str)


def load_cookie(browser, username_str):
    path = "Clients_Files/" + username_str + "/cookies_file"
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)


def LOAD_cookie(browser, username_str):
    browser.get('https://www.instagram.com/')
    # load cookies (with credentials inside)
    load_cookie(browser, username_str)
    browser.get('https://www.instagram.com/')
    time.sleep(3)


def click_first_pic(browser):
    time.sleep(2)
    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_aagw"))).click()
    except:
        print("Problem with first pic clicking")
        browser.close()
        exit()


def like_it(browser):
    try:
        like = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_aamw")))
        color = like.get_property("innerHTML")
        if "#8e8e8e" in color:
            time.sleep(random.uniform(2, 4))
            like.click()
            time.sleep(random.uniform(2, 4))
            return 1
        else:
            time.sleep(random.uniform(2, 4))
            return 0
    except:
        print("Problem with liking")
        browser.close()
        exit()


def put_likes(browser, target_of_likes):
    max_tryings = 5
    max_skip = 10
    for hash_i in hash_str:
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get("https://www.instagram.com/explore/tags/" + hash_i)
        click_first_pic(browser)
        liked = 0
        like_result = 0
        skip = 0
        tryings = 0
        while (liked < target_of_likes) and (skip < max_skip):
            try:
                try:
                    # If there is a restriction of actions IgBot detects it and stops
                    if WebDriverWait(browser, 5).until(
                            EC.visibility_of_element_located((By.XPATH, "//button[text()='Report a problem']"))) != 0:
                        WebDriverWait(browser, 5).until(
                            EC.visibility_of_element_located((By.XPATH, "//button[text()='Report a problem']"))).click()
                        print("Instagram detected a problem")
                    return
                except:
                    pass
                like_result = like_it(browser)
                liked += like_result
                if like_result == 1:
                    add_like(browser, hash_i, username_str)
                    skip = 0
                    tryings = 0
                else:
                    skip += 1
                    tryings = 0
                next(browser)
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


def next(browser):
    next_path = "//*[@aria-label='Next']"
    WebDriverWait(browser, 1).until(
        EC.visibility_of_element_located((By.XPATH, next_path))).click()
    # class name al 2023_01_22 '_ab6-'


# Returns string containing account's handle of current viewed post
def account_handle(browser):

    handle_handle = WebDriverWait(browser, 1).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='_aap6 _aap7 _aap8']")))

    return handle_handle[0].text


# Insert new line in Log file (da finire)
def add_like(browser, hashtag, username_str):
    try:
        line = pd.DataFrame({"Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                             "Tag": [hashtag],
                             "URL": [browser.current_url.split(".com")[1]],
                             "Sender": [username_str],
                             "Recipient": [account_handle(browser)]})
        csv_name = "Clients_Files/" + username_str + "/" + username_str + ".csv"
        line.to_csv(csv_name, index=False, header=False, mode='a')
    except:
        print("Problem with adding like on cvs")
