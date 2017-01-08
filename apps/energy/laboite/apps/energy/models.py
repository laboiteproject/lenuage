# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from datetime import timedelta
from django.db import models

from boites.models import Boite, App
from . import settings

import requests

class AppEnergy(App):
    url = models.URLField(_(u"URL du serveur emoncms"), help_text=_(u"Veuillez indiquer l'adresse de votre serveur emoncms"), default="https://emoncms.org/", null=False)
    power_feedid = models.PositiveSmallIntegerField(_(u"Identifiant flux puissance instantanée"), help_text=_(u"Veuillez saisir le numéro du flux lié à votre consommation instantannée (en watts)"), default=None, null=True)
    kwhd_feedid = models.PositiveSmallIntegerField(_(u"Identifiant flux consommation cumulée"), help_text=_(u"Veuillez saisir le numéro du flux lié à votre consommation cumulée (en kWh/j)"), default=None, null=True)
    emoncms_read_apikey = models.CharField(_(u"Clé d'API emoncms"), help_text=_(u"Veuillez indiquer votre clé d'API emoncms (lecture seule)"), max_length=32, default=None, null=True)

    power = models.PositiveSmallIntegerField(_(u"Consommation instantanée"), default=None, null=True)

    day0 = models.PositiveSmallIntegerField(_(u"Consommation j-6 (en kWh)"), default=None, null=True)
    day1 = models.PositiveSmallIntegerField(_(u"Consommation j-5 (en kWh)"), default=None, null=True)
    day2 = models.PositiveSmallIntegerField(_(u"Consommation j-4 (en kWh)"), default=None, null=True)
    day3 = models.PositiveSmallIntegerField(_(u"Consommation j-3 (en kWh)"), default=None, null=True)
    day4 = models.PositiveSmallIntegerField(_(u"Consommation j-2 (en kWh)"), default=None, null=True)
    day5 = models.PositiveSmallIntegerField(_(u"Consommation hier (en kWh)"), default=None, null=True)
    day6 = models.PositiveSmallIntegerField(_(u"Consommation aujourd'hui (en kWh)"), default=None, null=True)


    def get_app_dictionary(self):
        if self.enabled:
            self.power = None

            url = self.url
            url += "feed/timevalue.json?id="
            url += str(self.power_feedid)
            url += "&apikey="
            url += self.emoncms_read_apikey

            r = requests.get(url)

            self.power = int(float(r.json().get('value')))

            if True:
                now = timezone.now()
                last_week = now - timedelta(days=7)

                url = self.url
                url += "feed/data.json?id="
                url += str(self.kwhd_feedid)
                url += "&start="
                url += str(int(last_week.strftime('%s')) * 1000)
                url += "&end="
                url += str(int(now.strftime('%s')) * 1000)
                url += "&interval=86400&skipmissing=0&limitinterval=1&apikey="
                url += self.emoncms_read_apikey

                r = requests.get(url)

                values = r.json()

                #TODO : wow, crapy code spotted :
                try:
                    self.day0 = int(values[0].pop())
                    self.day1 = int(values[1].pop())
                    self.day2 = int(values[2].pop())
                    self.day3 = int(values[3].pop())
                    self.day4 = int(values[4].pop())
                    self.day5 = int(values[5].pop())
                    self.day6 = int(values[6].pop())
                except IndexError:
                    self.day0 = None
                    self.day1 = None
                    self.day2 = None
                    self.day3 = None
                    self.day4 = None
                    self.day5 = None
                    self.day6 = None

            self.save()

            return {'power' : self.power, 'day0': self.day0, 'day1': self.day1, 'day2': self.day2, 'day3': self.day3, 'day4': self.day4, 'day5': self.day5, 'day6': self.day6}

    class Meta:
        verbose_name = _("Configuration : Énergie")
        verbose_name_plural = _("Configurations : Énergie")
