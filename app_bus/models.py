# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.utils import dateparse
from datetime import timedelta
from django.db import models

from boites.models import Boite, App
from app_bus import settings

import requests

class AppBus(App):
    stop = models.PositiveSmallIntegerField(_(u"Arrêt"), help_text=_(u"Veuillez saisir l'identifiant Timeo de votre arrêt de bus"), default=None, null=True)

    route0 = models.CharField(_(u"Prochain bus"), max_length=4, default=None, null=True)
    departure0 = models.PositiveSmallIntegerField(_(u"Dans"), default=None, null=True)

    route1 = models.CharField(_(u"Bus suivant"), max_length=4, default=None, null=True)
    departure1 = models.PositiveSmallIntegerField(_(u"Dans"), default=None, null=True)

    def get_app_dictionary(self):
        if self.enabled:
            # we wan't to update every VALUES_UPDATE_INTERVAL minutes
            if self.last_activity is None or timezone.now() >= self.last_activity + timedelta(minutes=settings.VALUES_UPDATE_INTERVAL):
                url = 'https://data.explore.star.fr/api/records/1.0/search?dataset=tco-bus-circulation-passages-tr&rows=2&apikey=d55230a97e137bd4b073009462489f85d6486c1c242fb43db3d152a7&sort=-depart&refine.idarret='
                url += str(self.stop)

                r = requests.get(url)

                now = timezone.now()

                records = list(r.json()['records'])
                self.route0 = records[0]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[0]['fields']['depart']) - now
                self.departure0 = departure.seconds/60

                self.route1 = records[1]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[1]['fields']['depart']) - now
                self.departure1 = departure.seconds/60
                self.save()

            return {'route0' : self.route0, 'departure0': self.departure0, 'route1': self.route1, 'departure1':self.departure1}

    class Meta:
        verbose_name = _("Configuration : bus")
        verbose_name_plural = _("Configurations : bus")
