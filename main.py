from selenium.common.exceptions import TimeoutException
from definitions import *
# private variables and information are stored in inputs file
#       web_site = 'string'
#       username_str = 'string'
#       password_str = 'string'
#       hash_str = '#string'
#       no_cycle = number
from inputs import *


browser = lunch_browser(False, web_site)
cookies_accept(browser)
login(browser, username_str, password_str)
avoid_popups(browser)
search_hashtag(browser, hash_str)
click_first_pic(browser)

# crea variabili che contano il numero di post likati, quelli skipped e il numero di tentativi di refresh max
no_liked = 0
no_posts_seen = 0
max_tentativi = 0

# esegui una volta l'argomento del ciclo for perche' cambia l'xpath del bottone next
try:
    no_liked += like_if_its_ok(browser, no_liked)
    next_post = browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a")
    next_post.click()
except TimeoutException:  # Exception:
    print('non sono riuscito a caricare nemmeno la prima immagine')
    browser.close()
    exit()
no_posts_seen += 1

# esegui il ciclo
while no_liked < no_cycle:
    try:
        no_liked += like_if_its_ok(browser, no_liked)
        next_post = browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]")
        next_post.click()
        no_posts_seen += 1
    except TimeoutException:
        if max_tentativi == 3:
            browser.close()
            exit()
        back_n_forth(browser)
        max_tentativi += 1

# esegui l'ultimo visualizzato
no_liked += like_if_its_ok(browser, no_liked)
no_posts_seen += 1

# display stat
print('desiderati minimo:')
print(no_cycle)
print('ottenuti like: (ricorda che al massimo ne puo mettere due i piu dei desiderati)')
print(no_liked)
print('post osservati:')
print(no_posts_seen)

# close browser and exit
browser.close()

