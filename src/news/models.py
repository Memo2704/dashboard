# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Headline(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    last_scrape = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.last_scrape)
