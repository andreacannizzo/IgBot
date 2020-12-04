from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from inputs import *


def lunch_browser(images=True):
    if not images:
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options)
        browser.get('https://www.instagram.com/')
    else:
        browser = webdriver.Chrome(path_to_chromedriver)
        browser.get('https://www.instagram.com/')
    return browser


def cookies_accept(browser):
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//button[text()='Accetta']").click()


def login(browser, username_str_, password_str_):
    # inserisci username e password nei relativi slot
    username = browser.find_element_by_name('username')
    username.clear()
    username.send_keys(username_str_)
    password = browser.find_element_by_name('password')
    password.clear()
    password.send_keys(password_str_)
    # batti invio di conferma
    submit = browser.find_element_by_tag_name('form')
    submit.submit()


def avoid_popups(browser):
    # attendi pop up salvataggio credenziali e annullalo
    WebDriverWait(browser, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Non ora"]')).click()
    # attendi pop up attivazione notifiche e annullalo
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//button[text()='Non ora']").click()


def search_hashtag(browser, hash_str_='#lubitel'):
    # cerca barra ricerca, inserisci hashtag desiderato e batti due volte invio
    searchbox = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Cerca']")
        )
    )
    searchbox.send_keys(hash_str_)
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)


def click_first_pic(browser):
    # cerca prima immagine della pagina e cliccala
    first_image = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]")
        )
    )
    time.sleep(5)
    first_image.click()


def like_if_its_ok(browser, number):
    like_xpath = '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button'
    like = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, like_xpath)))
    color = like.get_property("innerHTML")
    if "#262626" in color:
        time.sleep(random.uniform(2, 4))
        like.click()
        print(number+1)
        time.sleep(random.uniform(2, 4))
        return 1
    else:
        time.sleep(random.uniform(3, 4))
        return 0


def back_n_forth(browser):
    time.sleep(10)
    print("torno indietro")
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[1]").click()
    time.sleep(10)
    print("torno avanti")
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()

