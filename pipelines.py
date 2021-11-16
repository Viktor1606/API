# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_bases = client['Scrapy_spider_vacsnsy']

    def process_item(self, item, spider):
        if item['salsry']:
            item['salary'] = self.edit_salary(item['salary'])

        name = ''.join(item['name'])
        salary_min = item['salary'][0]
        salary_max = item['salary'][1]
        salary_cur = item['salary'][2]
        link = item['url']
        site = item['site']

        vacancys_item = {'vacancys_name':name,
                         'salary_min': salary_min,
                         'salary_max': salary_max,
                         'salary_cur': salary_cur,
                         'link_vac': link,
                         'site': site
                         }
        collections = self.mongo_bases[spider.name]
        collections.update_one({'link_vac': vacancys_item['link_vac']},{'$set': vacancys_item}, upsert=True)


        return vacancys_item

    def edit_salary(self, salary):
        salary_min = None
        salary_max = None
        salary_cur = None

        if salary[0] == "ЗП не указана" or salary[0] == "По договоренности":
            salary_min = None
            salary_max = None
            salary_cur = None

        elif salary[0] == "до":
            salary_min = None
            salary_max = salary[2]
            salary_cur = salary[-1]

        elif len(salary) == 3 and salary[0].isdigit():
            salary_min = None
            salary_max = salary[0]
            salary_cur = salary[-1]

        elif salary[0] == "от":
            salary_min = salary[2]
            salary_max = None
            salary_cur = salary[-1]

        elif len(salary) > 3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]
            salary_cur = salary[-1]

        result = [salary_min, salary_max, salary_cur]
        return result