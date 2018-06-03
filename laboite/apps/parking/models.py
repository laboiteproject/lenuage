# coding: utf-8

from __future__ import unicode_literals

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES


class AppParking(App):
    UPDATE_INTERVAL = 5 * MINUTES

    CAR_PARK_CHOICES = (
        ('HFR', "Henri Fréville"),
        ('JFK', "J.F. Kennedy"),
        ('POT', "La Poterie"),
        ('PRE', "Les Préales"),
        ('VU', "Villejean-Université"),
    )
    parking = models.CharField(
        help_text=_("Veuillez sélectionner votre parking"),
        max_length=3,
        choices=CAR_PARK_CHOICES,
    )

    open = models.NullBooleanField(_('Parking ouvert ?'), default=None, null=True)
    available = models.PositiveSmallIntegerField(_('Places disponibles'), default=None, null=True)
    occupied = models.PositiveSmallIntegerField(_('Places occupées'), default=None, null=True)

    def should_update(self):
        return super(AppParking, self).should_update() or self.open is None

    def update_data(self):
        params = {
            'dataset': 'tco-parcsrelais-etat-tr',
            'rows': 1,
            'apikey': settings.STAR_API_KEY,
            'q': 'idparc={}'.format(self.parking)
        }

        self.open = None
        self.available = None
        self.occupied = None

        r = requests.get(settings.STAR_API_BASE_URL, params=params)

        records = r.json().get('records')
        if records:
            if records[0]['fields']['etat'] != "Fermé":
                self.open = True
                self.available = records[0]['fields']['nombreplacesdisponibles']
                self.occupied = records[0]['fields']['nombreplacesoccupees']
            else:
                self.open = False

        self.save()

    def _get_data(self):
        result = {
            'width': 32,
            'height': 10,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 9,
                    'x': 0,
                    'y': 0,
                    'color': 2,
					'font': 1,
					'content': '0xff839999839f9f9fff'
                },
                {
                    'type': 'text',
                    'width': len(str(self.available)) * 5,
                    'height': 8,
                    'x': 9,
                    'y': 2,
                    'color': 2,
					'font': 1,
					'content': '%s' % self.available,
                }
            ]
        }
        if not self.open:
            result['data'][1]['content'] = "Closed"
        return result

    class Meta:
        verbose_name = _('Configuration : parkings')
        verbose_name_plural = _('Configurations : parkings')
