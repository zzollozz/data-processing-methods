# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import re



class JopparserPipeline:
    def __init__(self):
        MONGO_HOST = '*****'
        MONGO_USER = "robot"
        MONGO_PASS = "****"

        server = SSHTunnelForwarder(
            MONGO_HOST,
            ssh_username=MONGO_USER,
            ssh_password=MONGO_PASS,
            remote_bind_address=('localhost', 27017)
        )
        server.start()

        client = MongoClient('localhost', server.local_bind_port)
        # client = MongoClient('localhost', 27017)    # создание клиента
        self.mongo_base = client.vacancy2001        # создали базу данных



    def process_item(self, item, spider): # сбор данных и назначение методов обработки для Данных
        if spider.name == 'hhru':
            item['salary'] = self.hhru_process_salary(item['salary'])

        elif spider.name == 'sjru':
            item['salary'] = self.sjru_process_salary(item['salary'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def hhru_process_salary(self, salary):  # метод обработки для зарплаты
        salary = ''.join(salary).split(' ')
        if salary[0] == 'от' and salary[2] == 'до':
            result = 'от', int(salary[salary.index('от') + 1].replace("\xa0", "")), 'до', int(
                salary[salary.index('до') + 1].replace("\xa0", "")), salary[-3]
        elif salary[0] == 'до':
            result = 'до', int(salary[salary.index('до') + 1].replace("\xa0", "")), salary[-3]
        elif salary[0] == 'от':
            result = 'от', int(salary[salary.index('от') + 1].replace("\xa0", "")), salary[-3]
        elif salary[0] == 'з/п':
            result = None
        return result

    def sjru_process_salary(self, salary):
        if salary[0] == 'По договорённости':
            result = None
        elif salary[0] == 'от':
            result = salary[salary.index('от') + 2].replace("\xa0", " ").split(' ')
            currency = salary[2]
            result = 'от', int(result[0] + result[1]), currency
        elif salary[0] == 'до':
            result = salary[salary.index('до') + 2].replace("\xa0", " ").split(' ')
            currency = salary[2]
            result = 'до', int(result[0] + result[1]), currency
        else:
            result = 'от', int(salary[0].replace("\xa0", "")), 'до', int(salary[1].replace("\xa0", "")), salary[3]
        return result