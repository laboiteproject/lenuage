# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.utils import dateparse
from datetime import timedelta
from django.db import models

from boites.models import Boite, App
from . import settings

import requests

class AppMetro(App):
    failure = models.BooleanField(_(u"Problème en cours ?"), default=False, null=False)
    recovery_time = models.PositiveSmallIntegerField(_(u"Minutes avant rétablissement"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.failure is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                url = 'https://data.explore.star.fr/api/records/1.0/search?dataset=tco-metro-lignes-etat-tr&rows=2&apikey='
                url += settings.STAR_API_KEY

                self.failure = False
                self.recovery_time = 0

                r = requests.get(url)

                now = timezone.now()
                records = r.json().get('records')
                if records:
                    records = list(records)

                    try:
                        if records[0]['fields']['etat'] != 'OK':
                            self.failure = True
                            self.recovery_time = int(records[0]['fields']['finpanneprevue'])
                    except IndexError:
                        pass

                self.save()

            return {'failure' : self.failure, 'recovery_time': self.recovery_time}

    class Meta:
        verbose_name = _("Configuration : Métro")
        verbose_name_plural = _("Configurations : Métro")
