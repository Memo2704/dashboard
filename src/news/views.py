# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import pytz
import requests
import os
import shutil
from .models import Headline, UserProfile
requests.packages.urllib3.disable_warnings()


def scrape(request):
    local_filename = ''
    user_p = UserProfile.objects.filter(user=request.user).first()
    if user_p is not None:
        user_p.last_scrape = datetime.now(timezone.utc)
        user_p.save()
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/51.0.2704.103 Safari/537.36"}
    url = 'https://theonion.com/'
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    posts = soup.find_all('div', {"class": 'sc-1whp23a-1 fUJpuS'})  # returns a list
    for i in posts:
        title = i.find_all('h4', {'class': 'sc-1qoge05-0 eoIfRA'})[0].text
        link = i.find_all('a', {'class': 'sc-1pw4fyi-3 jIlZnA js_link sc-1out364-0 fwjlmD'})[1]['href']

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.save()
    return redirect('/')
