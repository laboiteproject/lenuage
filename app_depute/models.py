# Create your models here.
#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals 
from django.utils.translation import ugettext as _
from django.db import models
from boites.models import Boite, App

import pycurl
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
import re
import math

url = "http://www2.assemblee-nationale.fr/scrutins/liste/%28legislature%29/" 
legislature = "14"
DEPUTE_COUNT = 577
presence_ratios = []


class AppDepute(App):
    
    presencePercentage = models.PositiveSmallIntegerField((u"Presence"),null=True, default=None)

    def get_app_dictionary(self):

        if self.enabled:

            buf = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
            c.setopt(c.WRITEDATA, buf)
            
            c.perform()
            c.close()
            
            body = buf.getvalue()
            
            soup = BeautifulSoup(body)
            
            votes = soup.findAll("table", attrs = {"class":"scrutins", "id":"listeScrutins"})[0].findAll("tbody")[0]
            
            for vote in votes.findAll("tr"):
                votes_for = int(vote.find("td", attrs = {"class":"pour"}).text)
                votes_against = int(vote.find("td", attrs = {"class":re.compile("contre *")}).text)
                votes_abst = int(vote.find("td", attrs = {"class":re.compile("abs *")}).text)
                presence = votes_for + votes_abst + votes_against
                ratio = float(presence) / DEPUTE_COUNT
                presence_ratios.append(ratio)
    
            self.presencePercentage = float(sum(presence_ratios)) / len(votes) * 100      
            self.save()

        return {'presence': self.presencePercentage}
    
    class Meta:
        verbose_name = _("Configuration : Deputes")
        verbose_name_plural = _("Configurations : Deputes")
