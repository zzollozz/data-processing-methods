# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder



class InstaparserPipeline:

    def __init__(self):
        MONGO_HOST = '******'
        MONGO_USER = "robot"
        MONGO_PASS = "1111"

        server = SSHTunnelForwarder(
            MONGO_HOST,
            ssh_username=MONGO_USER,
            ssh_password=MONGO_PASS,
            remote_bind_address=('localhost', 27017)
        )
        server.start()

        client = MongoClient('localhost', server.local_bind_port)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        print()
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item




























# class CSVPipeline(object):
#     ''' матод записи Йтома в CSV файл '''
#     def __init__(self):
#         self.file = 'database.csv'
#         with open(self.file, 'r', newline='') as csv_file:
#             self.tmp_data = csv.DictReader(csv_file).fieldnames
#
#         self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8')
#
#     def process_item(self, item, spider):
#         colums = item.fields.keys()
#
#         data = csv.DictWriter(self.csv_file, colums)
#         if not self.tmp_data:
#             data.writeheader()
#             self.tmp_data = True
#         data.writerow(item)
#         return item
#
#     def __del__(self):
#         self.csv_file.close()
