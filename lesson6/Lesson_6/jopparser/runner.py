from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jopparser import settings
from jopparser.spiders.hhru import HhruSpider
from jopparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()   # пустой объект без настроек
    crawler_settings.setmodule(settings) # закидываем настроки проекта с файла сетинг

    process = CrawlerProcess(settings=crawler_settings)      # создали пустую машину с настройками
    process.crawl(HhruSpider) # посадили водителя (нашего паука)
    process.crawl(SjruSpider) # посадили водителя (нашего паука)

    process.start()     # запуск

