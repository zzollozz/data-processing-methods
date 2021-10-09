"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
2. Сложить собранные новости в БД
"""
from pprint import pprint

import pymongo
from lxml import html
import requests
from sshtunnel import SSHTunnelForwarder

header = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
URL = 'https://lenta.ru/'

response = requests.get(URL)
dom = html.fromstring(response.text)
links_news = dom.xpath("//section[@class='b-yellow-box js-yellow-box']//@href")  # Выбераем новости с нужного блока
full_links_news = [] # собираем абсолютные ссыки в список
for link in links_news:
    full_links = (URL + link)
    full_links_news.append(full_links)

full_data_news = []   # результат список словарей с результатом

for link in full_links_news:    # перебираем ссылки по списку и заходим в каждую и выбераем то что нужно
    data = {}
    dom = html.fromstring((requests.get(link)).text)
    name_news = dom.xpath(".//h1[@class='b-topic__title']//text()")
    link_news = link
    publication_date = dom.xpath(".//time[@class='g-date']/text()")
    source = dom.xpath(".//div[@class='b-text clearfix js-topic__text']/p/a/text()")
    data['name_news'] = " ".join(name_news)
    data['link_news'] = link_news
    data['publication_date'] = " ".join(publication_date)
    data['source'] = "".join(source[0])
    full_data_news.append(data)

pprint(full_data_news)


MONGO_HOST = '192.168.1.76'
MONGO_DB = "news"
MONGO_USER = "robot"
MONGO_PASS = "1111"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)
server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
db = client[MONGO_DB]
data_news = db.news

for news in full_data_news:
    if data_news.find({'link_news': {'$ne': news.get('link_news')}}):
        pprint(news) # проверка выхода новых новостей
        data_news.insert_one(news)  # добавление новых новостей в базу





