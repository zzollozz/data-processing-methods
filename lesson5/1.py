a=1
""" Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
"""
import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


url = 'https://www.mvideo.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
chrome_options = Options()
chrome_options.add_argument("start-maximized")
path = '/Users/dzonsmitt/Desktop/Program/Data processing/lesson5/chromedriver'

driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get(url)

root = driver.find_element(By.TAG_NAME, 'html')

for i in range(3):
    root.send_keys(Keys.PAGE_DOWN)  # Пролистали страницу 3 раза
    time.sleep(1)

time.sleep(3)
button = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]") # Выбор кнопки В ТРЕНДЕ
button.click()

list_tov = driver.find_elements(By.XPATH, "//mvid-product-cards-group[@_ngcontent-serverapp-c254]//a")

link_cards = [i.get_attribute("href") for i in list_tov]

# pprint(link_cards)
list_card_goods = []


for el in range(0, len(link_cards), 3):
    list_card = {}
    link_card = link_cards[el]
    driver.get(link_card)
    time.sleep(3)
    name = driver.find_element(By.XPATH, "//h1[@class='title']").text
    price = driver.find_element(By.XPATH, "//mvid-price[@_ngcontent-serverapp-c321]//span[1]").text

    list_card['Имя товара:'] = name
    list_card['Цена товара:'] = price
    list_card['Ссылка на товар:'] = link_card

    list_card_goods.append(list_card)

pprint(list_card_goods)
driver.close()