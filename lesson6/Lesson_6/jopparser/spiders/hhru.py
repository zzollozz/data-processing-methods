import scrapy
from scrapy.http import HtmlResponse
from jopparser.items import JopparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=Python&from=suggest_post',
                  'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get() # перенесли вверх для работы многопоточности
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse) # получаем генератор который как бы выбирает нужную страницу и передает ее для обработки

        # next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        # if next_page:
        #         yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse): # логика обработки данный на выбранной странице
        name = response.xpath("//h1[@data-qa='vacancy-title']/text()").get()
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").getall()
        url_vacancy = response.url
        job_source = url_vacancy.split('/')[2]

        item = JopparserItem(name=name, salary=salary, url_vacancy=url_vacancy, job_source=job_source)
        yield item
