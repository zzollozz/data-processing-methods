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

from selenium.webdriver.support.ui import WebDriverWait # создание объекта задержки
from selenium.webdriver.support import expected_conditions as EC # ожидаемые события ( условия)
from selenium.common import exceptions as se


url = 'https://www.mvideo.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
chrome_options = Options()
chrome_options.add_argument("start-maximized")
path = '/Users/dzonsmitt/Desktop/Program/Data processing/lesson5/chromedriver'

driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get(url)

root = driver.find_element(By.TAG_NAME, 'html')

while True: # Ищем кнопку "в тренде" перелистывая страницы
    try:
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'В тренде')]")))
        button.click()
        break
    except se.TimeoutException:
        root.send_keys(Keys.PAGE_DOWN)


list_tov = driver.find_elements(By.XPATH, "//mvid-product-cards-group[@_ngcontent-serverapp-c254]//a")

link_cards = [i.get_attribute("href") for i in list_tov]

# pprint(link_cards)
list_card_goods = []

for el in range(0, len(link_cards), 3):
    list_card = {}
    link_card = link_cards[el]
    driver.get(link_card)

    wait = WebDriverWait(driver, 10)
    name = wait.until(EC.presence_of_element_located(((By.XPATH, "//h1[@class='title']"))))
    price = wait.until(EC.presence_of_element_located(((By.XPATH, "//mvid-price[@_ngcontent-serverapp-c321]//span[1]"))))

    list_card['Имя товара:'] = name.text
    list_card['Цена товара:'] = price.text
    list_card['Ссылка на товар:'] = link_card

    list_card_goods.append(list_card)

pprint(list_card_goods)
driver.close()