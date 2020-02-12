# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()


def scrape():
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/51.0.2704.103 Safari/537.36"}
    url = "https://www.theonion.com/"
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    columns = soup.find_all('div', {'class': 'sc-1whp23a-1 iUsrYc'})