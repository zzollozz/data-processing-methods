import scrapy
from scrapy.http import HtmlResponse
from leroy_merlen.items import LeroyMerlenItem
from scrapy.loader import ItemLoader



class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, qwery):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={qwery}&family=7f8ab360-4691-11ea-b7ce-8d83641e7e8e&suggest=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            # print('*' * 20, 'ПЕРЕШЕЛ НА СТРАНИЦУ', '*' * 20)
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='phytpj4_plp largeCard']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlenItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photo', "//img[@slot='thumbs']")
        loader.add_xpath('characteristic_key', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('characteristic_value', "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()


