import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

URL = 'https://giroskutershop.ru/ehlektrobajk-kupit-v-moskve'
url_path = 'https://giroskutershop.ru/'


def parser():
    r = requests.get(URL)
    html = BS(r.content, 'html.parser')
    url_bike = url_path + html.select(
        'body > div.site-wrapper > div.site-content-wrapper > div > div > div.product-list.product-list-thumbs > form:nth-child(1) > div.product-top > div.product-image > a')[
        0]['href']
    img = url_path + html.select(
        'body > div.site-wrapper > div.site-content-wrapper > div > div > div.product-list.product-list-thumbs > form:nth-child(1) > div.product-top > div.product-image > a > img')[
        0]['src']
    bike_name = html.select(
        'body > div.site-wrapper > div.site-content-wrapper > div > div > div.product-list.product-list-thumbs > form:nth-child(1) > div.product-top > div.product-image > a > img')[
        0]['alt']
    bike_description = html.select(
        'body > div.site-wrapper > div.site-content-wrapper > div > div > div.product-list.product-list-thumbs > form:nth-child(1) > div.product-top > div.product-anonce')[
        0].find_all('br')[0].text

    final_pars = (img, url_bike, bike_name, bike_description)
    print(f'Успешно спарсили данные с сайта {url_path}')
    return ''.join(final_pars)


with open('files/pars.txt', 'w') as file:
    file.write(parser())
print('Записали данные в файл pars.txt')
