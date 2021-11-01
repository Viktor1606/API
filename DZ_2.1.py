# https://spb.hh.ru/search/vacancy? fromSearchLine=true & text=Python & search_field=name &
# search_field=company_name & search_field=description
import requests
from bs4 import BeautifulSoup as bs
# from pprint import pprint

url = 'https://spb.hh.ru'
params = {'fromSearchLine': 'true',
          'text': 'Python',
          'search_field': 'name',
          'search_field': 'company_name',
          'search_field': 'description',
          'page': 1
          }
pages = int(input('Введ колличество страниц: '))
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}
vacancy_list = []
while params['page'] < pages:
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class': 'vacancy-serp-item'})

    if response.ok and vacancy:
        for vacans in vacancy:
            vacancy_data = {}
            info = vacans.find('a', {'class': 'bloko-link'})
            name = info.text
            link = info['href']
            company = vacans.find('a', {'class': 'bloko-link_secondary'}).text
            place = vacans.find('div', {'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).text
            site = url
            try:
                sal = vacans.find('div', {'class': 'vacancy-serp-item_sidebar'})
                s = sal.split()
                if ' - ' in sal:
                    sal_min, sal_max, sal_cur = int(s[0] + s[1]), int(s[3] + s[4]), s[5]
                elif ' от ' in sal:
                    sal_min, sal_max, sal_cur = int(s[1] + s[2]), None, s[3]
                elif ' до ' in sal:
                    sal_min, sal_max, sal_cur = None, int(s[1] + s[2]), s[3]
                else:
                    sal_min, sal_max, sal_cur = int([0] + s[1]), int(s[0] + s[1]), s[2]
            except:
                sal = None
                vacancy_data['name'] = name
                vacancy_data['link'] = link
                vacancy_data['company'] = company
                vacancy_data['place'] = place
                vacancy_data['sal_min'] = sal_min
                vacancy_data['sal_max'] = sal_max
                vacancy_data['sal_cur'] = sal_cur
                vacancy_list.append(vacancy_data)
            print(f"Найдено {params['page'] +1} страниц(а)")
            params['page'] += 1
        else:
            break
print()
