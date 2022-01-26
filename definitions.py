# set DISPLAY to 'remote' one
import os
os.environ["DISPLAY"] = ":0"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time
import random
import pickle


def launch_browser(path_to_chromedriver, images=True):
    chrome_options = webdriver.ChromeOptions()
    if images:
        chrome_options.add_experimental_option("prefs", {"intl.accept_languages": 'en,en_US'})
    else:
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,
                                                         'intl.accept_languages': 'en,en_US'})
    browser = webdriver.Chrome(path_to_chromedriver, options=chrome_options)
    return browser


def avoid_popup(browser, text_of_button):
    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//button[text()='" + text_of_button + "']").click()


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


def save_cookie(browser, username_str):
    os.makedirs("Clients_Files/" + username_str)
    path = "Clients_Files/" + username_str + "/cookies_file"
    with open(path, 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def SAVE_cookies(browser, username_str, password_str):
    browser.get('https://www.instagram.com/')
    avoid_popup(browser, "Accept All")
    login(browser, username_str, password_str)
    avoid_popup(browser, "Save Info")
    time.sleep(3)
    avoid_popup(browser, "Not Now")
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
    avoid_popup(browser, "Not Now")


def click_first_pic(browser):
    time.sleep(2)
    first_rec = "//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]"
    first_image = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, first_rec)))
    first_image.click()


def like_it(browser):
    like_xpath = "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button"
    like = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, like_xpath)))
    color = like.get_property("innerHTML")
    if "#8e8e8e" in color:
        time.sleep(random.uniform(2, 4))
        like.click()
        time.sleep(random.uniform(2, 4))
        return 1
    else:
        time.sleep(random.uniform(2, 4))
        return 0


def next(browser):
    next_path = "//*[@aria-label='Next']"
    WebDriverWait(browser, 1).until(
        EC.visibility_of_element_located((By.XPATH, next_path))).click()


# Returns string containing account's handle of current viewed post
def account_handle(browser):
    handle_xpath = "/html/body/div[6]/div[3]/div/article/div/div[2]/div/" \
                   "div/div[1]/div/header/div[2]/div[1]/div[1]/span/a"
    handle_handle = WebDriverWait(browser, 1).until(
        EC.visibility_of_element_located((By.XPATH, handle_xpath)))
    return handle_handle.text


# Insert new line in Log file (da finire)
def add_like(browser, hashtag, username_str):
    line = pd.DataFrame({"Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                         "Tag": [hashtag],
                         "URL": [browser.current_url.split(".com")[1]],
                         "Sender": [username_str],
                         "Recipient": [account_handle(browser)]})
    csv_name = "Clients_Files/" + username_str + "/" + username_str + ".csv"
    line.to_csv(csv_name, index=False, header=False, mode='a')
