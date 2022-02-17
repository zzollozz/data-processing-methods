# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy as scrapy
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import csv


class LeroyMerlenPipeline:

    def __init__(self):
        MONGO_HOST = '192.168.1.74'
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
        self.mongo_base = client.leroymerlen        # создали базу данных

    def process_item(self, item, spider):
        item['characteristic'] = self.process_characteristic(item)
        del item['characteristic_key']
        del item['characteristic_value']
        # item['photo'] = self.item_completed(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_characteristic(self, item):
        key = item['characteristic_key']
        value = [' '.join(val.split()) for val in item['characteristic_value']]
        characteristic = dict(zip(key, value))
        return characteristic


class LeroyMerlenPhotoPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        value = item['photo']
        value = [i.split('"')[3] for i in value]
        if value:
            for img in value:
                try:
                    img = img.replace('82', '2000', 2)
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        pass
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        product = item['name']
        category = product.split()[0]
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{category}/{product}/{image_guid}.jpg"

class CSVPipeline(object):
    ''' матод записи item в CSV файл '''
    def __init__(self):
        self.file = 'database.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8')

    def process_item(self, item, spider):
        colums = item.fields.keys()

        data = csv.DictWriter(self.csv_file, colums)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item

    def __del__(self):
        self.csv_file.close()