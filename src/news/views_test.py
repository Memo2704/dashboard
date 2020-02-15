from django.shortcuts import render
import re
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()


def scrape():

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/51.0.2704.103 Safari/537.36"}
    url = 'https://www.lanacion.com.ar/'
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    posts = soup.find_all('section', {"class": 'content-apertura-50 place-22'})
    title_names = soup.findAll(class_='content-titulo')
    for tile in title_names:
        print(tile.text)

    # for name in title_names:
    #     names = name.contents[1].renderContents()
    #     m = re.findall(r'>(.*?)<', str(names))
    #     if m is None and m ==
    #     print(m)
    # for title in title_names:
    #     print(title['volanta'])
    # try:
    #     for i in posts:
    #         # link = i.find_all('a', {'class': 'sc-1pw4fyi-1 kwykKR js_link sc-1out364-0 fwjlmD'})[0]['href']
    #         title = i.find('h2', {'class': 'content-titulo'}).text
    #         # image_source = i.find('img', {'class': 'dv4r5q-2 iaqrWM'})['srcset']
    #         # print(link)
    #         print(title)
    #         # print(image_source)
    # except TypeError as e:
    #     print(e)


scrape()
