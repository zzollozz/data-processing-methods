# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import qwery as qwery
import scrapy
from itemloaders.processors import MapCompose, TakeFirst

# characteristic_value[0].replace('\n', '').split()
def int_prise(value):
    try:
        value = int(value)
    except:
        return value
    return value


class LeroyMerlenItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_prise), output_processor=TakeFirst())
    link = scrapy.Field()
    photo = scrapy.Field()
    characteristic_key = scrapy.Field()
    characteristic_value = scrapy.Field()
    characteristic = scrapy.Field()
    _id = scrapy.Field()
    pass
