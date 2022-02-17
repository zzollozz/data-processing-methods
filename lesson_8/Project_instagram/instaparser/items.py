# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # id_user_parse = scrapy.Field()
    username_for_parse = scrapy.Field()
    url_user_parse = scrapy.Field()
    media_count_full_name_parse = scrapy.Field()
    business_count_name_parse = scrapy.Field()
    list_followers_users = scrapy.Field()
    list_following_users = scrapy.Field()
    _id = scrapy.Field()

