# coding: utf-8

from __future__ import unicode_literals

import requests
from django.db import models
from django.utils.translation import ugettext as _

from boites.models import App, MINUTES
from . import settings


class AppMetro(App):
    UPDATE_INTERVAL = 30 * MINUTES

    failure = models.BooleanField(_('Problème en cours ?'), default=False, null=False)
    recovery_time = models.PositiveSmallIntegerField(_('Minutes avant rétablissement'), default=None, null=True)

    def update_data(self):
        url = 'https://data.explore.star.fr/api/records/1.0/search'
        params = {'dataset': 'tco-metro-lignes-etat-tr',
                  'rows': 2,
                  'apikey': settings.STAR_API_KEY}
        self.failure = False
        self.recovery_time = 0

        r = requests.get(url, params=params)
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

    def _get_data(self):
        if not self.failure:
            return None
        return {'failure': self.failure,
                'recovery_time': self.recovery_time}

    class Meta:
        verbose_name = _("Configuration : métro")
        verbose_name_plural = _("Configurations : métro")
