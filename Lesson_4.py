import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news_bd']
persons = db.persons
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}


resource = requests.get('https://yandex.ru/news/')
dom = html.fromstring(resource.text)
items = dom.xpath('//article[contains(@class,"mg-card_type_image")]')
news = []
for item in items:
    new = {}
    news_name = item.xpath('.//h2[@class="mg-card__title"]/text()')
    source = item.xpath('.//a[@class="mg-card__source-link"]/text()')
    links = item.xpath('.//h2[@class="mg-card__title"]/../@href')
    time = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    new['news_name'] = news_name
    new['source'] = source
    new['links'] = links
    new['time'] = time
    news.append(new)

    persons.insert_one(new)
pprint(news)
