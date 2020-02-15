# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from pytz import timezone
import requests
import os
import shutil
from .models import Headline, UserProfile
requests.packages.urllib3.disable_warnings()


def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    user_p.last_scrape = datetime.now(timezone("utc"))
    user_p.save()
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/51.0.2704.103 Safari/537.36"}
    url = "https://www.theonion.com/"
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    posts = soup.find_all('div', {'class': 'sc-1whp23a-1 iUsrYc'})

    for i in posts:
        link = i.find_all('a', {'class': 'sc-1pw4fyi-1 kwykKR js_link sc-1out364-0 fwjlmD'})[0]['href']
        title = i.find_all('h4', {'class': 'sc-1qoge05-0 eoIfRA'})[0].text
        image_source = i.find('img', {'class': 'sc-1dm5z0l-0 bUrcfY'})['src']

        # stackoverflow solution
        media_root = '/home/tony/PycharmProjects/dashboard/media_root'
        if not image_source.startswith(("data:image", "javascript")):
            local_filename = image_source.split('/')[-1].split("?")[0]
            r = session.get(image_source, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)
        # end of the so solution

            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = local_filename
            new_headline.save()
        return redirect('/')
