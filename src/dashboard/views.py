import math
from datetime import datetime, timedelta, timezone, tzinfo
from django.shortcuts import render, redirect

from news.models import Headline, UserProfile
from notepad.forms import NoteModelForm
from notepad.models import Note


ZERO = timedelta(0)


class UTC(tzinfo):

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


def home(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    now = datetime.now(utc)
    time_diff = now - user_p.last_scrape
    time_diff_hours = time_diff / timedelta(minutes=60)
    next_scrape = 24 - time_diff_hours
    if next_scrape <= 24:
        hide_me = True
    else:
        hide_me = False
    headlines = Headline.objects.all()
    notes = Note.objects.filter(user=request.user)

    form = NoteModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/home/')
    context = {
        'form': form,
        'notes_list': notes,
        'object_list': headlines,
        'hide_me': hide_me,
        'next_scrape': math.ceil(next_scrape)
    }
    return render(request, 'news/home.html', context)
