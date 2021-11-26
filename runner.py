from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerua.spiders.leroymerlin import leruakatalogSpider
from lerua import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('Введите поисковый запрос: ')
    process.crawl(leruakatalogSpider, query='стеллаж')
    process.start()
