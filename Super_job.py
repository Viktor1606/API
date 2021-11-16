import scrapy
from scrapy.http import HtmlResponse
from jobparser.spiders.items import JobparserItem

class Super_jobSpider(scrapy.Spider):
    name = 'Super_job'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class= "icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//span[@class = "_1e6dO _1XzYb _2EZcW"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]/text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)