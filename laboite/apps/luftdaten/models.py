# coding: utf-8
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.models import App

import requests


class AppLuftdaten(App):
    sensor = models.CharField(_('Identifiant du capteur Luftdaten'),
                              help_text=_("Veuillez saisir l'identifiant de votre capteur luftdaten"), max_length=32,
                              default=_('11034'), null=False, blank=False)

    AQI_CHOICES = (
        (0, _('Bon')),
        (1, _('Moyen')),
        (2, _('Mauvais')),
    )
    aqi = models.PositiveSmallIntegerField(_("Qualité de l'air mesuré par votre capteur"), choices=AQI_CHOICES,
                                           default=0)

    def _get_data(self):
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 10,
                    'height': 8,
                    'x': 0,
                    'y': 0,
                    'color': 1,
                    'content': '0x081422419455417f',
                },
                {
                    'type': 'bitmap',
                    'width': 2,
                    'height': 2,
                    'x': 8,
                    'y': 12,
                    'color': 1,
                    'content': '0x800',
                },
                {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 10,
                    'y': 1,
                    'color': 2,
                    'font': 1,
                    'content': self.AQI_CHOICES[self.aqi][1],
                },
            ]
        }

    def update_data(self):
        self.aqi = 0

        r = requests.get(settings.LUFTDATEN_URL + self.sensor + '/')

        pm = max(
            r.json()[1].get('sensordatavalues')[0].get('value'),
            r.json()[1].get('sensordatavalues')[1].get('value')
        )
        if float(pm) < 25.0:
            self.aqi = 0
        elif float(pm) < 50.0:
            self.aqi = 1
        else:
            self.aqi = 2
        self.save()

    class Meta:
        verbose_name = _('Configuration : luftdaten')
        verbose_name_plural = _('Configurations : luftdaten')
