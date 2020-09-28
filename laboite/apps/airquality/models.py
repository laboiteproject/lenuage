# coding: utf-8
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App, MINUTES

import requests


class AppAirQuality(App):
    UPDATE_INTERVAL = 30 * MINUTES

    aqi_today = models.PositiveSmallIntegerField(_("Qualité de l'air pour aujourd'hui"), default=0)

    def _get_data(self):
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 10,
                    'x': 0,
                    'y': 0,
                    'color': 1,
                    'content': '0x6010e202fc00f0081000',
                },
                {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 10,
                    'y': 1,
                    'color': 2,
                    'content': self.convert_airbzh_atmo(self.aqi_today),
                },
            ]
        }

    def update_data(self):
        self.aqi_today = 0

        r = requests.get(settings.AIRBZH_URL)

        for feature in r.json().get('features'):
            if 'Rennes' in feature['properties']['lib_zone']:
                self.aqi_today = int(feature['properties']['valeur'])
        self.save()

    def convert_airbzh_atmo(self, aqi):
        if aqi < 5:
            return "Bon"
        elif aqi < 8:
            return "Moyen"
        else:
            return "Mauvais"

    class Meta:
        verbose_name = _('Configuration : qualité de l\'air')
        verbose_name_plural = _('Configurations : qualité de l\'air')
