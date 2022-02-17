from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy_merlen import settings
from leroy_merlen.spiders.lmru import LmruSpider  # импорт класса из паука



if __name__ == '__main__':
    crawler_settings = Settings()   # пустой объект без настроек
    crawler_settings.setmodule(settings) # закидываем настроки проекта с файла сетинг

    process = CrawlerProcess(settings=crawler_settings)      # создали пустую машину с настройками
    process.crawl(LmruSpider, qwery='Обои') # посадили водителя (нашего паука)
    process.start()     # запуск