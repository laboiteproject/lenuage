# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.utils import dateparse
from datetime import timedelta
from django.db import models

from boites.models import App
from . import settings

import requests


class AppBus(App):
    UPDATE_INTERVAL = 60
    API_BASE_URL = 'https://data.explore.star.fr/api/records/1.0/search'

    stop = models.PositiveSmallIntegerField(_('Arrêt'), help_text=_("Veuillez saisir l'identifiant Timeo de votre arrêt de bus"), default=None, null=True)
    route0 = models.CharField(_('Prochain bus'), max_length=4, default=None, null=True)
    departure0 = models.PositiveSmallIntegerField(_('Dans'), default=None, null=True)

    route1 = models.CharField(_('Bus suivant'), max_length=4, default=None, null=True)
    departure1 = models.PositiveSmallIntegerField(_('Dans'), default=None, null=True)

    def should_update(self):
        return super(AppBus, self).should_update() or self.route0 is None

    def update_data(self):
        params = {
            'dataser': 'tco-bus-circulation-passages-tr',
            'rows': 2,
            'apikey': settings.STAR_API_KEY,
            'sort': '-depart',
            'q': 'idarret={}'.format(self.stop)
        }

        self.route0 = None
        self.departure0 = None
        self.route1 = None
        self.departure1 = None

        r = requests.get(self.API_BASE_URL, params=params)

        now = timezone.now()
        records = r.json().get('records')
        if records:
            records = list(records)

            try:
                self.route0 = records[0]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[0]['fields']['depart']) - now
                self.departure0 = departure.seconds / 60
            except IndexError:
                self.route0 = None
                self.departure0 = None

            try:
                self.route1 = records[1]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[1]['fields']['depart']) - now
                self.departure1 = departure.seconds / 60
            except IndexError:
                self.route1 = None
                self.departure1 = None

        self.save()

    def _get_data(self):
        return {'route0': self.route0,
                'departure0': self.departure0,
                'route1': self.route1,
                'departure1': self.departure1}

    class Meta:
        verbose_name = _('Configuration : bus')
        verbose_name_plural = _('Configurations : bus')
