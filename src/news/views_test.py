from django.shortcuts import render
import re
import unicodedata
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()


def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/51.0.2704.103 Safari/537.36"}
    url = 'https://www.nytimes.com/'
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    posts = soup.find('div', {"class": 'css-k2t2rg'})
    title_list = []
    for title in posts:
        data = title.findAll('div', {'class': 'css-1ez5fsm esl82me1'})
        for i in data:
            title_list.append(i.text)

    link_list = []
    for div in posts.find_all('div', {'class': 'css-6p6lnl'}):
        for a in div.find_all('a'):
            link_list.append(a['href'])

    images = soup.find_all('img', {'src': re.compile('.jpg')})
    images_source = []
    for image in images:
        images_source.append(image['src']+'\n')
        elements_source = map(unicode.strip, images_source)

    # convert the lists of data into a dict
    d1 = {}
    d1.setdefault('notice_1', []).append(title_list[0])
    d1.setdefault('notice_1', []).append(link_list[0])
    d1.setdefault('notice_1', []).append(elements_source[0])
    d1.setdefault('notice_2', []).append(title_list[1], )
    d1.setdefault('notice_2', []).append(link_list[1])
    d1.setdefault('notice_2', []).append(elements_source[1])
    d1.setdefault('notice_3', []).append(title_list[2])
    d1.setdefault('notice_3', []).append(link_list[2])
    d1.setdefault('notice_3', []).append(elements_source[2])
scrape()