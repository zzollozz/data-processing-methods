import scrapy
from scrapy.http import HtmlResponse
from jopparser.items import JopparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ bs_sM _3ze9n l9LnJ f-test-button-dalshe f-test-link-Dalshe']/@href").get() # перенесли вверх для работы многопоточности
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse) # получаем генератор который как бы выбирает нужную страницу и передает ее для обработки


    def vacancy_parse(self, response: HtmlResponse): # логика обработки данный на выбранной странице
        name = response.xpath("//h1[@class='rFbjy mWAI4 _3DjcL _3fXVo']/text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _3a-0Y _3DjcL _3fXVo']/text()").getall()
        url_vacancy = response.url
        job_source = url_vacancy.split('/')[2]

        item = JopparserItem(name=name, salary=salary, url_vacancy=url_vacancy, job_source=job_source)
        yield item
